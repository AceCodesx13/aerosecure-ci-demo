# 4. First SageMaker AI training job

Finish the local guide first. The AWS route uses the same training script inside a mentor-built CPU container. No permanent prediction endpoint is required by this starter.

## Step 1: Obtain the mentor's configuration

The mentor supplies approved AWS sign-in, region, private S3 bucket, team prefix, SageMaker execution role, ECR training-image digest, permitted CPU instance and spending limit. Obtain a completed `config/aws.json` based on `config/aws.example.json`. Do not guess account or resource identifiers.

The mentor must complete `docs/06_MENTOR_SETUP.md`. A notebook workspace such as SageMaker Studio JupyterLab is optional. You can also submit from your laptop using approved temporary AWS credentials. Never paste access keys into files or notebooks.

## Step 2: Install the AWS client libraries

From the package root, using the environment Python from the local guide:

```text
PYTHON -m pip install -r requirements-aws.txt
```

Authenticate using your institution's approved temporary-credential workflow. If the mentor uses AWS IAM Identity Center, they should provide the profile name and `aws sso login --profile <profile>` instructions. For a named profile set `AWS_PROFILE` to the supplied profile. In PowerShell: `$env:AWS_PROFILE = "your-approved-profile"`. In Bash: `export AWS_PROFILE="your-approved-profile"`. Studio-managed credentials may need no profile. The scripts do not create credentials.

## Step 3: Print the smoke-run plan

```text
PYTHON aws/submit_training.py
```

This command makes **no AWS calls**. It prints a proposed request using 800 training and 200 validation rows. Read the account, role, image, instance, input paths, output path and runtime limit. The script rejects placeholders, mismatched account/region image names and unsuitable starter resource sizes.

The plan does not calculate cost or verify service quotas. Confirm the mentor has checked current regional prices, access, CPU quota and spending allowance. Runtime limits bound training time but do not eliminate storage or other charges.

## Step 4: Submit one paid smoke job

```text
PYTHON aws/submit_training.py --execute
```

The script verifies the signed-in account and bucket region, uploads only `train.csv` and `validation.csv` from `data/smoke/`, then starts one CPU job. It never uploads raw orders or the final test file.

It prints a job name such as `capstone-smoke-...` and saves a submission record under `artifacts/aws/`. Record this exact name. The call returns after submission; it does not wait for completion.

The container reads `/opt/ml/input/data/train/train.csv` and `/opt/ml/input/data/validation/validation.csv`. It writes `model.joblib` to `/opt/ml/model` and `validation_metrics.json` to `/opt/ml/output/data`. SageMaker uploads these as model/output archives under the configured run prefix.

## Step 5: Check the job

Replace `YOUR_JOB_NAME` with the printed job name:

```text
PYTHON aws/check_job.py YOUR_JOB_NAME
```

Expected progression includes `InProgress` and then `Completed`. For `Failed`, inspect `FailureReason` and CloudWatch logs with the mentor. Do not repeatedly launch new jobs to diagnose a permission problem.

To stop your unwanted active training job:

```text
PYTHON aws/check_job.py YOUR_JOB_NAME --stop
```

The command requests stopping; check again to confirm the final state. Already completed jobs cannot be stopped. Retained S3 files still remain.

## Step 6: Run the full release after the smoke job succeeds

First print the full plan, then execute it within the permitted spend:

```text
PYTHON aws/submit_training.py --dataset full
PYTHON aws/submit_training.py --dataset full --execute
```

The full job uploads 10,614 training rows and 2,469 validation rows under a different prefix. It fits a new model. The tiny smoke model is for infrastructure validation, not final accuracy comparisons.

## Step 7: Retrieve and evaluate the frozen cloud model

In the SageMaker console, open the completed full job. Find its S3 model artifact location, also printed by `check_job.py`. In the private S3 console download **your own run's** `model.tar.gz`. Download `output.tar.gz` from the same job output directory for its validation report.

Extract the model archive into `artifacts/cloud/model/` and the output archive into `artifacts/cloud/reports/`. Verify you have `artifacts/cloud/model/model.joblib` and the validation report. Review package versions and the selected experiment before opening the final test set. Use Python 3.12 and the package's pinned libraries locally.

```text
PYTHON src/predict.py --model artifacts/cloud/model/model.joblib --output artifacts/cloud/predictions.csv
PYTHON src/evaluate.py --model artifacts/cloud/model/model.joblib --output artifacts/cloud/reports
```

This evaluates the cloud model locally using the same held-out CSV and evaluation code. It does not upload the test set or create a prediction endpoint. Only load trusted artifacts from your own course job; joblib files can execute code when loaded.

## Step 8: Save evidence and stop idle workspace compute

Save the submission record, job name, model URI, data hashes, image digest, validation report and final test report. Stop idle Studio/JupyterLab applications if you used them. The mentor decides which S3 artifacts and ECR images to retain. Do not delete shared resources.

## Troubleshooting

| Symptom | Likely action |
|---|---|
| Placeholder rejection | Ask the mentor for the completed configuration. |
| No credentials / wrong account | Fix your approved sign-in/profile, then reprint the plan. |
| `AccessDenied` on upload or job start | Mentor checks team-prefix permissions, `iam:PassRole`, execution role and ECR access. |
| Quota / instance unavailable | Mentor selects an allowed CPU instance and checks region/quota. |
| Container fails to start | Mentor verifies Linux amd64 image, image digest, entrypoint and source build. |
| Model source differs from local code | Rebuild and approve a new image. Do not treat it as the same experiment. |

The package has been checked locally. Live AWS execution still depends on the mentor's account setup and a successful smoke run.
