import json
import os
import sys

# checks the metrics from train.py and fails the build if the model
# doesnt beat both baselines
# run: python .github/scripts/quality_gate.py artifacts/reports/validation_metrics.json

if len(sys.argv) < 2:
    print("need the path to validation_metrics.json")
    sys.exit(2)

with open(sys.argv[1]) as f:
    report = json.load(f)

# make sure we never gate on the test split by accident
if report["evaluation_split"] != "validation":
    print("FAIL: metrics are not from the validation split")
    sys.exit(1)

model = report["model"]
quoted = report["quoted_baseline"]
median = report["historical_median_baseline"]

passed = model["mae_days"] < quoted["mae_days"] and model["mae_days"] < median["mae_days"]

# markdown table so the results show up on the actions page
out = "## Smoke training results (validation split)\n\n"
out += "| Predictor | MAE (days) | RMSE (days) | Underestimate rate |\n"
out += "|---|---|---|---|\n"

for name, m in [("Model (random forest)", model), ("Quoted lead time baseline", quoted), ("Historical median baseline", median)]:
    out += f"| {name} | {m['mae_days']} | {m['rmse_days']} | {m['underestimate_rate']} |\n"

out += f"\nRows: {report['row_count']} | Trees: {report['parameters']['trees']} | Python {report['versions']['python']} | scikit-learn {report['versions']['sklearn']}\n\n"

if passed:
    out += "**Gate: PASS** - model beats both baselines"
else:
    out += "**Gate: FAIL** - model does not beat both baselines"

print(out)

# this env variable only exists when running on github, so skip it locally
if "GITHUB_STEP_SUMMARY" in os.environ:
    with open(os.environ["GITHUB_STEP_SUMMARY"], "a") as f:
        f.write(out + "\n")

if not passed:
    sys.exit(1)
