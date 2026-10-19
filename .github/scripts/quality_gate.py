"""Quality gate for the smoke training run.

Reads the validation_metrics.json that src/train.py writes and fails the
CI job if the model does not beat BOTH baselines on validation MAE.
Also writes a small markdown table to the GitHub job summary so you can
see the numbers without opening the logs.

Usage: python .github/scripts/quality_gate.py <path/to/validation_metrics.json>
"""
import json
import os
import sys
from pathlib import Path


def main():
    if len(sys.argv) != 2:
        print("usage: quality_gate.py <validation_metrics.json>")
        return 2

    report = json.loads(Path(sys.argv[1]).read_text())

    # the gate should only ever look at validation, never the test split
    if report.get("evaluation_split") != "validation":
        print("FAIL: metrics are not from the validation split")
        return 1

    model = report["model"]["mae_days"]
    quoted = report["quoted_baseline"]["mae_days"]
    median = report["historical_median_baseline"]["mae_days"]

    rows = [
        ("Model (random forest)", report["model"]),
        ("Quoted lead time baseline", report["quoted_baseline"]),
        ("Historical median baseline", report["historical_median_baseline"]),
    ]
    beats_both = model < quoted and model < median

    lines = [
        "## Smoke training results (validation split)",
        "",
        "| Predictor | MAE (days) | RMSE (days) | Underestimate rate |",
        "|---|---|---|---|",
    ]
    for name, m in rows:
        lines.append(f"| {name} | {m['mae_days']} | {m['rmse_days']} | {m['underestimate_rate']} |")
    lines += [
        "",
        f"Rows: {report['row_count']} | Trees: {report['parameters']['trees']} | "
        f"Python {report['versions']['python']} | scikit-learn {report['versions']['sklearn']}",
        "",
        "**Gate: PASS** - model beats both baselines" if beats_both
        else "**Gate: FAIL** - model does not beat both baselines",
    ]
    summary = "\n".join(lines)
    print(summary)

    summary_file = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_file:
        with open(summary_file, "a") as f:
            f.write(summary + "\n")

    return 0 if beats_both else 1


if __name__ == "__main__":
    sys.exit(main())
