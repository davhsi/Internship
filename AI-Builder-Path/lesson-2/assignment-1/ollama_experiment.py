"""Prompt rendering, Ollama calls, and result persistence for the lab."""

from __future__ import annotations

import json
import os
import socket
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from experiment_data import BILLING_POLICY, SCENARIOS


PROJECT_DIR = Path(__file__).resolve().parent
PROMPTS_DIR = PROJECT_DIR / "prompts"
OUTPUTS_DIR = PROJECT_DIR / "outputs"
OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = os.getenv("OLLAMA_MODEL", "qwen3:8b")
OLLAMA_TIMEOUT_SECONDS = int(os.getenv("OLLAMA_TIMEOUT_SECONDS", "300"))
OLLAMA_NUM_PREDICT = int(os.getenv("OLLAMA_NUM_PREDICT", "700"))
OLLAMA_NO_THINK = os.getenv("OLLAMA_NO_THINK", "").lower() in {"1", "true", "yes"}


def load_prompt(filename: str) -> str:
    return (PROMPTS_DIR / filename).read_text(encoding="utf-8")


def build_prompt(template: str, scenario: dict[str, str]) -> str:
    prompt = (
        template.replace("{{billing_policy}}", BILLING_POLICY.strip())
        .replace("{{account_details}}", scenario["account_details"])
        .replace("{{customer_question}}", scenario["customer_question"])
    )
    if OLLAMA_NO_THINK:
        prompt += "\n\n/no_think"
    return prompt


def ask_ollama(prompt: str) -> str:
    payload = json.dumps(
        {
            "model": MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
            "options": {"temperature": 0.2, "num_predict": OLLAMA_NUM_PREDICT},
        }
    ).encode("utf-8")
    request = Request(OLLAMA_URL, data=payload, headers={"Content-Type": "application/json"})

    try:
        with urlopen(request, timeout=OLLAMA_TIMEOUT_SECONDS) as response:
            body = json.loads(response.read().decode("utf-8"))
    except HTTPError as error:
        raise RuntimeError(f"Ollama returned HTTP {error.code}: {error.read().decode('utf-8', 'replace')}") from error
    except (TimeoutError, socket.timeout) as error:
        raise RuntimeError(
            f"Ollama timed out after {OLLAMA_TIMEOUT_SECONDS} seconds. "
            "Try rerunning the script, using a smaller model, or increasing "
            "`OLLAMA_TIMEOUT_SECONDS`."
        ) from error
    except URLError as error:
        raise RuntimeError(
            "Cannot reach Ollama. Start it with `ollama serve` (or open the Ollama app), "
            "then ensure the selected model has finished downloading."
        ) from error

    content = body["message"]["content"].strip()
    if not content:
        raise RuntimeError(
            "Ollama returned an empty response. Rerun the same command; the script "
            "will keep completed responses and retry missing ones by default."
        )

    return content


def write_results(filename: str, prompt_label: str, results: list[dict[str, str]]) -> None:
    OUTPUTS_DIR.mkdir(exist_ok=True)
    payload = {
        "model": MODEL,
        "prompt_label": prompt_label,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "results": results,
    }
    (OUTPUTS_DIR / filename).write_text(json.dumps(payload, indent=2), encoding="utf-8")


def load_existing_results(filename: str) -> list[dict[str, str]]:
    path = OUTPUTS_DIR / filename
    if not path.exists():
        return []

    payload = json.loads(path.read_text(encoding="utf-8"))
    return [
        result
        for result in payload.get("results", [])
        if result.get("response", "").strip()
    ]


def run_experiment(
    label: str,
    template_file: str,
    output_file: str,
    prompt_label: str,
    fresh: bool,
    scenario_ids: set[str],
    keep_going: bool,
) -> list[dict[str, str]]:
    template = load_prompt(template_file)
    results = [] if fresh else load_existing_results(output_file)
    completed_ids = {result["scenario_id"] for result in results}

    for scenario in SCENARIOS:
        if scenario_ids and scenario["id"] not in scenario_ids:
            continue

        if scenario["id"] in completed_ids:
            print(f"Skipping {label}: {scenario['id']} already completed.")
            continue

        print(f"Running {label}: {scenario['id']}...")
        prompt = build_prompt(template, scenario)
        result = {
            "scenario_id": scenario["id"],
            "customer_question": scenario["customer_question"],
            "expected_behavior": scenario.get("expected_behavior", ""),
            "response": "",
        }
        try:
            result["response"] = ask_ollama(prompt)
        except RuntimeError as error:
            if not keep_going:
                raise
            result["error"] = str(error)
            print(f"Error for {scenario['id']}: {error}", file=sys.stderr)
        results.append(result)
        write_results(output_file, prompt_label, results)
    return results
