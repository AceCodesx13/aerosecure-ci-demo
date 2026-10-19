# 1. Local setup and first training run

## Step 1: Extract and open the package

Extract the ZIP to a normal folder. Open a terminal in `ASU_Capstone_Student_Starter`. Confirm you can see `README.md`, `requirements.txt`, `data`, and `src`. Do not run commands from inside `src`.

Install Python 3.12 if it is not already available. On Windows, check `py -3.12 --version`. On macOS/Linux, check `python3.12 --version`.

## Step 2: Create your Python environment

Windows PowerShell:

```powershell
py -3.12 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

macOS/Linux:

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

In the remaining examples, **`PYTHON` means your environment's Python executable**. Replace `PYTHON` with `.venv\Scripts\python.exe` on Windows or `.venv/bin/python` on macOS/Linux. No activation command is required.

Do not type the literal word `PYTHON`. For example, the next command on Windows is `.venv\Scripts\python.exe src/validate_data.py`.

If you prefer one command after installing requirements, use `.venv\Scripts\python.exe src/run_local.py` on Windows or `.venv/bin/python src/run_local.py` on macOS/Linux. It runs validation, baselines, training, prediction and rule examples in order. It does **not** evaluate the final test split. The numbered steps below explain each action.

## Step 3: Validate the supplied release

```text
PYTHON src/validate_data.py
PYTHON -m unittest discover -s tests -v
```

Expected: a line beginning `PASS` from validation, and `OK` from the tests. The validator checks counts, catalog links, timestamps, exact label values, train/validation/test separation and release file hashes.

If a hash check fails, you changed a supplied CSV. Restore the release or regenerate a separate dataset. Do not delete the check to make the result pass.

## Step 4: Establish the baselines

```text
PYTHON src/baseline.py
```

Expected: validation metrics for quoted lead time and historical median delivery time. The historical median uses training rows only, grouped by part category. It falls back to the global training median for an unknown category.

Output: `artifacts/reports/baseline_metrics.json`. Lower `mae_days` is better. `underestimate_rate` is the fraction of orders where the prediction was shorter than actual delivery.

## Step 5: Train locally

```text
PYTHON src/train.py
```

The script fits a CPU random forest on the **training** file and evaluates on **validation**. It does not read the test file. It encodes categorical fields and handles missing input values inside a pipeline fitted on training data only.

Expected outputs:

- `artifacts/model/model.joblib`: the model, preprocessing pipeline and planning margin.
- `artifacts/reports/validation_metrics.json`: model/baseline metrics, parameters, input hashes and dependency versions.

Allow a few minutes on a laptop. To change the number of trees, use `PYTHON src/train.py --trees 160`. Compare changes on validation only. The default model path is overwritten by another run. Save each useful run in a separate directory:

```text
PYTHON src/train.py --trees 160 --model-dir artifacts/run-02/model --reports-dir artifacts/run-02/reports
```

## Step 6: Predict five example orders

```text
PYTHON src/predict.py
```

Expected: five rows with typical predicted days and conservative delivery days. Output: `artifacts/predictions.csv`.

The five inputs have no delivery target. They are illustrative copies of test-period input records, not a new independent evaluation set. Do not use them to estimate model accuracy. For your own predictions, create a CSV with `order_id` and all features in `docs/02_DATA_GUIDE.md`, then pass `--input your_file.csv`.

The conservative estimate adds the 90th percentile of validation underprediction residuals and rounds upward. It is a planning estimate, not guaranteed delivery or statistically certified coverage.

## Step 7: Run the separate rules

```text
PYTHON src/policy_demo.py
```

Expected: nine shipment decisions, three maintenance results, and two access examples followed by `PASS`. Read `docs/03_POLICY_GUIDE.md` to explain the results.

## Step 8: Freeze your experiment, then evaluate on test

Before running this step, record your selected features, parameters and validation result in `docs/05_EXPERIMENT_AND_HANDOFF.md`. Stop changing the model for this release.

```text
PYTHON src/evaluate.py
```

Expected outputs: `artifacts/reports/test_metrics.json` and `artifacts/reports/test_predictions.csv`. The script evaluates the saved model and never fits it. It reports overall error, error by part group and conservative coverage.

If you used run-02, pass `--model artifacts/run-02/model/model.joblib --output artifacts/run-02/reports`. Keep the final test result even if it is disappointing. Do not tune against it. A new round of development needs a newly reserved evaluation period.

## Optional notebook route

Install `requirements-notebooks.txt` instead of the basic requirements, then run `PYTHON -m jupyterlab` from the package root. Open these notebooks in order:

1. `01_inspect_and_baseline.ipynb`
2. `02_train_and_predict.ipynb`
3. `03_frozen_model_test.ipynb` only after freezing the experiment

Each notebook locates the package root and calls the same scripts. Do not run both routes repeatedly just to reproduce the same run.

## Troubleshooting

| Symptom | Action |
|---|---|
| Python command not found | Install Python 3.12 or use its full executable path. |
| `ModuleNotFoundError` | Install requirements with the same environment Python used to run scripts. |
| File not found | Open the terminal in the extracted package root. |
| Slow first training | Wait for completion. Close other large jobs. Use `--trees 40` for a smaller local smoke run. |
| Changed schema or hash failure | Restore the supplied release. Make experiments in a new folder. |
| Cannot load a cloud model | Use the exact Python and package versions recorded in its metrics. Only load artifacts from your trusted course run. |

## Regeneration, after the first run

`PYTHON src/generate_data.py --output regenerated` creates a separate copy of the CSV dataset. The default seed is `20261012`. The same seed and generator reproduce the same data hashes. `--seed 42` creates a different dataset. Do not silently replace the class evaluation release. Raw orders, prepared files and the manifest must always come from one generation run.
