# 6. Mentor setup and release responsibilities

Students can begin locally immediately. The AWS instructions intentionally depend on real account details supplied by the mentor. This package does not launch services or publish data on its own.

## Before releasing the package

Confirm the fictional label definitions and training-release scope. This ZIP contains no operational aircraft/supplier data. Treat `data/prepared/` as the approved synthetic classroom derivative. If adapting to real information, conduct a separate release review covering inputs, models, logs and predictions. Do not reclassify a dataset merely by dropping its label column.

Agree numerical model acceptance criteria after the pilot and before the final test. Keep the supplied test release fixed. An instructor wanting a genuinely hidden final test must withhold `data/prepared/test/` and issue it at the review; the distributed starter includes it for a self-contained teaching exercise. The generator formula is visible, so this is an educational benchmark, not a blind competitive evaluation.

## AWS prerequisite checklist

1. Confirm account ownership, funding, regional CPU quota and initial permitted spend.
2. Provide individual temporary sign-in. Use least-privilege team roles rather than shared long-lived keys.
3. Create a private same-region S3 bucket with Block Public Access, encryption, appropriate retention and versioning.
4. Create a SageMaker execution role trusted by `sagemaker.amazonaws.com`. Permit reading only the team's approved train/validation prefixes and writing the run outputs. Grant ECR image-pull and CloudWatch logging permissions. If using KMS, configure matching key permissions.
5. Permit students to upload the approved training files, start/describe/stop their training jobs, read their output artifacts, inspect bucket location, and pass only the approved execution role to SageMaker. Limit `iam:PassRole` with the passed-to-service condition where applicable.
6. Set budgets/alerts and review the current regional prices. Alerts may lag charges. The starter uses one CPU instance and a default 1,800-second runtime limit.
7. Build the image below, test it locally, publish an immutable version and give students its digest URI.
8. Complete `config/aws.json`, then supervise one smoke run. No live cloud success is claimed until that run completes.

These are responsibilities rather than a universal IAM policy. Studio, VPC-only access, KMS and institutional identity requirements vary. A VPC-only deployment may require approved service endpoints and a VPC configuration added to the request by the account administrator.

## Build the training image

Use a mentor workstation with Docker and the AWS CLI. Run from the extracted package root. The Dockerfile copies `src/` and installs the exact training dependencies. Select Linux amd64 to match the approved x86 CPU instances.

```text
docker build --platform linux/amd64 -f aws/Dockerfile -t capstone-training:1.0.0 .
```

To perform a local container smoke test on Windows PowerShell, from the package root:

```powershell
$packagePath = (Get-Location).Path
New-Item -ItemType Directory -Force artifacts/docker/model,artifacts/docker/output | Out-Null
docker run --rm --network none -v "${packagePath}/data/smoke/train:/opt/ml/input/data/train:ro" -v "${packagePath}/data/smoke/validation:/opt/ml/input/data/validation:ro" -v "${packagePath}/artifacts/docker/model:/opt/ml/model" -v "${packagePath}/artifacts/docker/output:/opt/ml/output/data" capstone-training:1.0.0
```

For macOS/Linux use the same Docker mounts with the absolute package path and create the output folders first. Verify `model.joblib` and `validation_metrics.json`. Docker is a mentor prerequisite, not necessary for student local training.

Authenticate to the approved same-region ECR registry using the AWS CLI's ECR login flow. Create a private repository, tag the image with its exact repository URI, and push version `1.0.0`. Record the repository image's `sha256` digest using `aws ecr describe-images`. Supply students the **digest URI** `ACCOUNT.dkr.ecr.REGION.amazonaws.com/REPOSITORY@sha256:DIGEST`, not a mutable latest tag.

Fill all placeholders in `config/aws.example.json` and save as `config/aws.json`. Keep a separate team prefix for each team. The starter's request checks same account and region. Approve the chosen CPU size rather than assuming `ml.m5.large` is available. If you modify dependencies or source code, build a new image version and record its digest.

The base Docker tag is mutable during builds. For an audited release, resolve and pin `python:3.12-slim` by digest before building, and preserve the image dependency inventory. Students use the finished ECR digest, so the submitted artifact stays fixed.

## Actual access-control exercise

The local `can_read()` function is a simulation. S3 does not inspect CSV row labels automatically. To enforce the proposed tiers:

1. Partition raw records into distinct object prefixes such as `raw/unrestricted/`, `raw/restricted/` and `raw/highly-restricted/` using the label values.
2. Keep any combined raw file under the most restrictive controlled location. Do not place a mixed-classification CSV in the student-readable prefix.
3. Grant student roles only the unrestricted raw tier and the explicitly approved training derivative. Mentors can read restricted raw records. Administrators can read all tiers.
4. Enforce the same access model for derived artifacts and deny unintended alternate access paths. Apply account/institution policy where it is stricter than this fictional example.
5. Test allow and deny cases using real roles. Preserve denied access evidence and confirm public access remains blocked.

The submission script uploads no raw data. It also does not configure or certify the tier permissions. Mentor setup is essential if access enforcement is part of the assessment.

To create local tier files for this exercise, run `PYTHON src/create_access_tiers.py` using the environment Python from the local guide. It writes three CSVs under `artifacts/access-tiers/` and performs no AWS calls. The mentor uploads these only to the corresponding controlled prefixes after verifying permissions. Tier totals must sum to 20,000.

## Teaching alignment

The updated slides introduce labels now, then policy integration after initial training. They describe Studio as the proposed workspace. This package also supports a local notebook client and uses a custom CPU training container to keep the training program consistent. S3 still supplies input files and receives model/report artifacts. No GPU, language-model API or permanent endpoint is required.
