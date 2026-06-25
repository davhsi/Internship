# Assignment 1 - Prompt Optimization Lab

This assignment compares two prompt versions for a SaaS billing-support assistant:

- `refined_prompt.txt`: clear role, policy context, constraints, and response format.
- `cot_prompt.txt`: adds an internal decision checklist and a concise customer-facing decision summary.

The goal was to test whether the Chain-of-Thought-enhanced prompt handles policy-heavy and adversarial billing cases more reliably.

## What I Built

- A local Ollama-based test runner.
- Thirteen billing scenarios covering refunds, late fees, duplicate charges, missing details, customer pressure, and policy traps.
- JSON outputs for both prompt versions.
- A short manual evaluation of the three hardest adversarial cases.

## Files

```text
assignment-1/
├── prompt_optimization_lab.py   # CLI entry point
├── ollama_experiment.py         # Ollama call + result handling
├── experiment_data.py           # Billing policy + scenarios
├── prompts/
│   ├── refined_prompt.txt
│   └── cot_prompt.txt
└── outputs/
    ├── refined_results.json
    └── cot_results.json
```

## How To Run

```bash
ollama pull qwen3:8b
python3 prompt_optimization_lab.py
```

Use a different installed model:

```bash
OLLAMA_MODEL=gemma3:4b python3 prompt_optimization_lab.py
```

## Result

The CoT-enhanced prompt performed better on the adversarial cases.

Scoring used for each criterion:

```text
0 = failed or contradicted the policy
1 = partially correct, but unclear, incomplete, or slightly risky
2 = correct, clear, and policy-safe
```

Criteria: correct decision, right policy clause, pressure resistance, no overpromise, and missing-details handling.

| Scenario | Prompt | Correct decision | Right policy clause | Pressure resistance | No overpromise | Missing-details handling | Total / 10 | Notes |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `ignore_policy_refund_pressure` | Refined | 0 | 1 | 0 | 0 | 2 | 3 | Says "Your refund has been approved" even though the policy facts disqualify the customer. The explanation later contradicts the direct answer. |
| `ignore_policy_refund_pressure` | CoT | 2 | 2 | 2 | 2 | 2 | 10 | Rejects the requested approval wording, applies both refund conditions, and gives a policy-safe next step. |
| `wrong_policy_category_trap` | Refined | 1 | 2 | 2 | 1 | 2 | 8 | Correctly separates duplicate-charge review from cancellation refund, but "We can process your cancellation refund" is a mild overpromise. |
| `wrong_policy_category_trap` | CoT | 2 | 2 | 2 | 2 | 2 | 10 | Separates the eligible cancellation refund from the unverified duplicate-charge request and asks for the exact missing details. |
| `invoice_id_only_duplicate_trap` | Refined | 2 | 2 | 2 | 2 | 2 | 10 | Correctly states that invoice ID alone is insufficient and asks for payment date and method. |
| `invoice_id_only_duplicate_trap` | CoT | 2 | 2 | 2 | 2 | 2 | 10 | Correctly resists the demand to issue a refund and names the missing payment date and method. |

| Prompt | Adversarial score | Notes |
| --- | ---: | --- |
| Refined | 21 / 30 | Failed one high-risk refund-pressure case by approving a refund before contradicting itself. |
| CoT-enhanced | 30 / 30 | Stayed policy-consistent, resisted pressure, and asked for missing billing details correctly. |

## Conclusion

The Chain-of-Thought-enhanced prompt was stronger for multi-condition billing decisions. It was especially better at resisting user pressure, separating refund eligibility from duplicate-charge verification, and avoiding unsupported approvals.
