# ASU Capstone student starter package

Start here. This package teaches a supplier delivery-time model using fictional orders. It also includes separate exercises for data access, shipment policy and maintenance arithmetic.

## What you will build

Predict **calendar days from supplier acceptance to receipt of the full ordered quantity in usable condition**. Compare your predictions with two simple baselines. Save the model and show that another student can reproduce your result.

Aircraft names are real. Suppliers, regions, order histories, restrictions and maintenance scenarios are fictional. Every aircraft–part association and `SIM-` part number is illustrative and is not verified compatibility. This package is not an aircraft maintenance or procurement authority.

## Package contents

| Location | Purpose |
|---|---|
| `docs/01_LOCAL_START.md` | Numbered setup, baseline, training and prediction instructions |
| `docs/02_DATA_GUIDE.md` | Definitions, file map, chronological splits and data dictionary |
| `docs/03_POLICY_GUIDE.md` | Both restriction systems and worked examples |
| `docs/04_AWS_STUDENT_GUIDE.md` | Mentor-ready SageMaker workflow |
| `docs/05_EXPERIMENT_AND_HANDOFF.md` | Evaluation protocol and student submission template |
| `docs/06_MENTOR_SETUP.md` | Cloud prerequisites, container build and access-control responsibilities |
| `docs/07_SOURCES_AND_ASSUMPTIONS.md` | Sources and the boundary between real facts and simulation |
| `docs/REFERENCE_TABLE_SCHEMAS.md` | Field names and examples for every reference catalog |
| `docs/REFERENCE_RUN.md` | Instructor reference results and verification boundaries |
| `slides/` | Companion five-slide Monday training overview |
| `data/reference/` | 20 aircraft models, 20 part categories, 400 associations, 9 suppliers, 3 regions and policy tables |
| `data/raw/orders.csv` | 20,000 completed synthetic orders, including policy metadata |
| `data/prepared/` | Fixed training, validation and test CSVs with approved model columns |
| `data/smoke/` | Small training and validation subsets for the first paid job |
| `data/examples/` | Five prediction examples and deterministic policy/maintenance scenarios |
| `data/manifest.json` | Release version, seed, split counts and SHA-256 hashes |
| `notebooks/` | Three optional notebooks following the same sequence as the command-line guide |
| `src/` | Reproducible generation, validation, baseline, training and policy code |
| `aws/` | Mentor Dockerfile and student plan/submit/status commands |
| `tests/` | Checks for policy, chronological isolation and cloud request configuration |

## Start in this order

1. Open `docs/01_LOCAL_START.md`. Finish the local workflow first. No AWS account is needed.
2. Read `docs/02_DATA_GUIDE.md` while inspecting the catalogs and sample records.
3. Run the restriction and maintenance examples in `docs/03_POLICY_GUIDE.md`.
4. Use `docs/04_AWS_STUDENT_GUIDE.md` only after the mentor completes cloud setup.
5. Complete `docs/05_EXPERIMENT_AND_HANDOFF.md` for your lab review.

Use Python **3.12** for the starter. Run all commands from this folder, where this README and `requirements.txt` live. Choose either the command-line route or the notebooks. Both use the same scripts and CSVs.

## Fixed release rules

- Do not use the test split to select features, tune parameters or choose a model.
- Do not add usable receipt dates, actual delivery days or future approvals to model inputs.
- Keep data-access classification separate from shipment restriction.
- The ZIP is an authorized fictional teaching release. Labels inside it demonstrate a policy; a local CSV does not enforce access control. Operational restricted data must never enter this release.
- The AWS path uploads only the approved training derivative, never the raw catalog/order file or final test split.
- Account, bucket, role, image and spending approval must come from the mentor. The package does not create AWS resources automatically.

The cloud route uses a mentor-built CPU container so SageMaker runs the **same `src/train.py` and dependency versions** as the local route. Keep code changes synchronized with the image. Changing local source does not change an existing image.
