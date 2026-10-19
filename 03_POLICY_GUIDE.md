# 3. Two separate restriction systems

These are the proposed fictional classroom definitions used by the updated slides. The exact labels are **Unrestricted**, **Restricted**, and **Highly Restricted**. They do not represent actual export-control classifications or institutional data classifications.

## Data access

| Data label | Simulated roles that may read it |
|---|---|
| Unrestricted | Student, mentor, administrator |
| Restricted | Mentor, administrator |
| Highly Restricted | Administrator |

Unrestricted means accessible to approved project participants, not public on the internet. An unknown label or role receives no access. `can_read()` in `src/policy.py` demonstrates that rule. It does not prevent someone opening a local file.

The distributed package contains only fictional teaching data. Everyone receiving this release is authorized to inspect the synthetic examples, including rows carrying example restriction labels. The role matrix becomes a real access exercise only when the mentor places records into separately controlled AWS locations.

A mentor must explicitly approve a derived training release. For this fictional starter, `data/prepared/` is the approved release and may be used by students. It excludes policy/audit metadata but contains underlying fictional order features. For real data, field removal alone does not reduce classification or authorize disclosure. Model artifacts, logs and predictions can also reveal information and need appropriate access controls.

## Shipment eligibility

| Shipment label | Rule in this simulation |
|---|---|
| Unrestricted | No special authorization. Destination must still be eligible. |
| Restricted | Eligible destination plus `Valid` authorization. Missing/expired authorization requires review. |
| Highly Restricted | Eligible destination plus explicit `Approved after review` status. Ordinary valid authorization is insufficient. |

The matrix allows Regions A/B/C for Unrestricted and Restricted shipments. Highly Restricted allows Regions A/B and blocks Region C. Unknown label/destination requires review. Review-required means no automatic approval. A human approval cannot override an explicitly blocked destination in this matrix.

These rules are examples chosen for the classroom and must not be interpreted as real country restrictions. Any real compliance requirements would need a separately approved policy.

## Examples

- A tire order can have Restricted data access and Unrestricted shipment eligibility. Those labels answer different questions.
- A Highly Restricted shipment to Region C stays blocked even if an approval record exists.
- A Restricted shipment to Region A with expired authorization requires review.
- A fast lead-time prediction cannot change a blocked shipment into an allowed one.

Run `PYTHON src/policy_demo.py` using the Python path defined in the local guide. It checks `data/examples/policy_scenarios.csv`, maintenance examples and access examples.

## Maintenance integration

The maintenance scenario projects days to need as `ceil(max(0, interval_hours − hours_since_replacement) / projected_daily_flight_hours)`. It adds those days to the scenario date. These are invented classroom intervals, not manufacturer maintenance requirements.

Latest order date equals need date minus conservative delivery days minus buffer days. An allowed candidate with an order deadline already in the past requires escalation. A blocked candidate stays blocked. If every candidate is blocked or infeasible, the system must report no feasible option and escalate. The supplied scenario code demonstrates individual candidates; students must add multi-supplier selection for the integrated fall prototype.

## Timing for the semester

Introduce and validate labels during data preparation now. Complete the first baseline and training run. Then implement and test policy enforcement and combine it with maintenance calculations before the December demonstration. Cloud access control starts before any restricted data upload, not after training.
