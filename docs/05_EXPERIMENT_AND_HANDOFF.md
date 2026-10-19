# 5. Experiment record and lab handoff

## Success for the starter

First prove the workflow is reproducible. Validation and tests pass, the baseline runs, training writes a model and validation report, and prediction produces five rows. A cloud smoke job adds infrastructure evidence when AWS is ready.

For model evaluation, compare MAE against both baselines. Report the actual result, whether improved or not. A development target is a lower validation MAE than the strongest baseline. Do not invent a required accuracy threshold. Students and mentors must agree numerical acceptance criteria before the final review, after inspecting the pilot results.

The release has a conservative estimate calibrated from the validation residuals. Report its measured test coverage and mean excess days. High coverage obtained by extremely large margins may be operationally unhelpful. Report error separately for consumables, repairables and major components.

Do not claim real procurement accuracy from synthetic results. Report maturity-filtering bias, clean inputs, fictional routes, unobservable disruption shocks, and unverified part compatibility.

## Experiment record template

Copy this section for each selected run:

```text
Team and run identifier:
Dataset version and seed:
Training and validation file SHA-256:
Code revision or release SHA-256:
Local Python and dependency versions:
Model algorithm and parameters:
Feature list or feature changes:
Quoted baseline validation MAE:
Historical median validation MAE:
Model validation MAE:
Validation underestimation rate:
Conservative margin and validation coverage:
Decision to retain/reject this run and why:
Frozen experiment date:
Final test MAE and both baseline MAEs:
Final test conservative coverage / excess days:
Error by part group:
AWS job name, region, image digest and model URI, if used:
Reproduction steps:
Limitations and remaining work:
```

## Suggested student responsibilities

Students choose their own assignments. Useful areas are data/schema validation, baseline/model development, policy/maintenance integration and reproducibility/AWS evidence. Every student should explain the target and the separation between prediction and authorization.

## Starter handoff checklist

- [ ] Validation and policy tests pass.
- [ ] Train/validation/test files remain separate.
- [ ] Another student reproduces the chosen local run.
- [ ] Model and reports identify input hashes and package versions.
- [ ] Final test results are preserved without tuning against them.
- [ ] Policy examples demonstrate allowed, blocked and review-required outcomes.
- [ ] Maintenance examples demonstrate a recommendation and an escalation.
- [ ] AWS smoke/full job evidence is saved if cloud access is ready.
- [ ] Idle compute and ongoing resource ownership are documented.

## Work remaining for the full fall prototype

This starter is a training foundation. Students still need to assemble current multi-supplier simulation snapshots, connect model predictions to explicit maintenance/policy rules, rank eligible candidates, handle no-feasible-option cases, and document the integrated lab demonstration. The final reviewer determines whether the complete evidence supports the scoped TRL-4 target.
