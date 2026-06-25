"""Compare refined and Chain-of-Thought-enhanced billing prompts with Ollama."""

from __future__ import annotations

import os
import sys
from argparse import ArgumentParser

from ollama_experiment import run_experiment


def parse_args() -> tuple[str, bool, set[str], bool]:
    parser = ArgumentParser(description="Compare billing-support prompts with Ollama.")
    parser.add_argument(
        "--prompt",
        choices=("all", "refined", "cot"),
        default=os.getenv("PROMPT_FILTER", "all"),
        help="Which prompt set to run. Defaults to all. Can also use PROMPT_FILTER.",
    )
    parser.add_argument(
        "--fresh",
        action="store_true",
        help="Start from scratch instead of keeping completed responses from the output JSON.",
    )
    parser.add_argument(
        "--scenario",
        action="append",
        default=os.getenv("SCENARIO_IDS", "").split(",") if os.getenv("SCENARIO_IDS") else [],
        help="Run only this scenario ID. Repeat the flag for multiple scenarios. Can also use comma-separated SCENARIO_IDS.",
    )
    parser.add_argument(
        "--keep-going",
        action="store_true",
        help="Save an error for failed scenarios and continue with later scenarios.",
    )
    args = parser.parse_args()
    return args.prompt, args.fresh, set(args.scenario), args.keep_going


def main() -> int:
    prompt_filter, fresh, scenario_ids, keep_going = parse_args()
    try:
        if prompt_filter in ("all", "refined"):
            run_experiment(
                "refined prompt",
                "refined_prompt.txt",
                "refined_results.json",
                "Refined Prompt",
                fresh,
                scenario_ids,
                keep_going,
            )
        if prompt_filter in ("all", "cot"):
            run_experiment(
                "CoT prompt",
                "cot_prompt.txt",
                "cot_results.json",
                "Chain-of-Thought-Enhanced Prompt",
                fresh,
                scenario_ids,
                keep_going,
            )
    except RuntimeError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    print("Done. Results saved in outputs/.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
