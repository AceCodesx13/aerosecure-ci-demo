# Instructor reference run

The starter was executed locally with Python 3.12.14 and the pinned training dependencies. These are observed results for the supplied seed, not student acceptance requirements.

| Metric | Validation | Test |
|---|---:|---:|
| Quoted baseline MAE, days | 6.559 | 7.113 |
| Historical median baseline MAE, days | 14.975 | 16.542 |
| Model MAE, days | 5.244 | 5.810 |
| Conservative coverage | 90.04% | 87.89% |

Validation-calibrated coverage does not guarantee the same coverage on later records. Test mean conservative excess was 8.604 days. See `REFERENCE_RUN.json` for full metrics and group breakdowns.

Checks completed: dataset validation, seven unit tests, baseline, local training, five-row prediction, nine shipment cases, three maintenance cases, test evaluation, generator reproducibility, training-channel simulation and AWS request-shape validation. Notebook code cells were compiled and notebook structure checked. The notebooks are intentionally unexecuted for students.

No Docker image was built and no live AWS job was launched. The mentor must build/approve the training image, configure the account and complete the first cloud smoke run.
