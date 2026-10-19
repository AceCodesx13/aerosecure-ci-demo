# 2. Data definitions and file map

## One row and the prediction target

One historical row is one **completed order for one illustrative aircraft–part association from one supplier**. `quantity_ordered` is the number of individual units, not packages. Suppliers in this simplified exercise specialize in a part group and can supply every illustrative category in that group.

`actual_delivery_days` is calendar days from supplier acceptance to the date the **full quantity is received in usable condition**. All dates use ISO `YYYY-MM-DD` and day-level resolution. No weekends or holidays are removed. The clean starter excludes cancellations and partial deliveries. Those are later extensions because they require a different target/censoring definition.

## Catalog scope

There are 20 models across five manufacturers: 6 Airbus, 5 Boeing, 4 Embraer, 2 ATR and 3 De Havilland Canada. They cover single-aisle jets, widebody jets, regional jets and turboprops. This is a historical model mix, not a claim about current production.

Each model has 20 illustrative categories: 8 consumables, 8 common repairable items and 4 major assemblies. That is **16 common items plus 4 major components**, giving 400 associations. The major categories are engine assembly, landing-gear assembly, environmental control unit and flight-control actuator assembly. We use an environmental control unit rather than assuming every aircraft has the same auxiliary-power-unit configuration. No specific compatibility is certified.

Consumables use condition `New`. Repairable and major items can be `New`, `Repaired` or `Overhauled`. Synthetic suppliers have different handling and replenishment patterns. Regions A/B/C have no real geographic mapping. Route transit and customs allowances are known planning inputs at acceptance, not actual future transit outcomes.

## File relationships

`aircraft_models.csv` and `part_categories.csv` join through `aircraft_parts.csv`. Orders reference aircraft models, part categories and suppliers by stable IDs. `suppliers.csv` defines origin and specialty. `supplier_eligibility.csv` lists valid category/supplier combinations. `routes.csv` defines each origin/destination pair. `shipment_policy.csv` defines destination eligibility by shipment label.

## Fixed chronological splits

| Split | Accepted orders | Outcome must be known before | Rows |
|---|---|---|---:|
| Train | Before 2025-01-01 | 2025-01-01 | 10,614 |
| Validation | 2025-01-01 through 2025-04-30 | 2025-05-01 | 2,469 |
| Test | 2025-05-01 onward | 2026-09-30 | 3,749 |
| Excluded at boundary | Earlier orders still awaiting usable receipt at the relevant boundary | Recorded in audit CSV | 3,168 |

The raw dataset contains 20,000 orders. The prepared splits contain 16,832. Exclusion prevents training or validation with outcomes that were still in the future at the simulated development boundary. This maturity filtering can underrepresent slow outstanding orders. Report that limitation and consider censored/outstanding-order methods in later work.

Split files preserve the same columns. IDs and accepted dates support tracing and splitting but are **not model features**. The training script reads only the feature allowlist in `src/schema.py`.

## Order data dictionary

| Field | Meaning and valid values | Role |
|---|---|---|
| `order_id` | Unique `ORD-` identifier | Trace only |
| `accepted_date` | Supplier acceptance date | Split/trace only |
| `aircraft_model_id` | Foreign key to aircraft catalog | Categorical feature |
| `part_category_id` | Foreign key to part-category catalog | Categorical feature |
| `supplier_id` | Foreign key to supplier catalog | Categorical feature |
| `condition` | `New`, `Repaired`, `Overhauled`, subject to category | Categorical feature |
| `origin_region_id` | Supplier location, `REG-A/B/C` | Categorical feature |
| `destination_region_id` | Order destination, `REG-A/B/C` | Categorical feature |
| `quantity_ordered` | Positive integer units | Numeric feature |
| `stock_at_acceptance` | Nonnegative available supplier units at acceptance | Numeric feature |
| `supplier_backlog_days` | Nonnegative quoted workload allowance at acceptance | Numeric feature |
| `quoted_lead_time_days` | Positive supplier quote, calendar days, known at acceptance | Numeric feature |
| `route_transit_days` | Nonnegative planned route transit allowance | Numeric feature |
| `route_customs_days` | Nonnegative planned customs allowance | Numeric feature |
| `order_month` | Integer 1–12, derived from acceptance date | Numeric feature |
| `actual_delivery_days` | Positive calendar-day elapsed delivery outcome | Target, never an input |
| `usable_receipt_date` | Actual full-quantity usable receipt date | Raw audit only, never an input |
| `order_status` | `Completed` in this release | Raw metadata |
| `data_access_classification` | `Unrestricted`, `Restricted`, `Highly Restricted` | Separate access policy |
| `shipment_restriction_classification` | Same three exact labels | Separate shipment policy |
| `authorization_status_at_acceptance` | `Not required`, `Valid`, `Approved after review` in completed history | Raw policy metadata |
| `authorization_recorded_date` | On/before acceptance when authorization is required, otherwise blank | Raw audit metadata |
| `source_type` | `Synthetic` | Provenance |

There are 13 model features: six categorical and seven numeric. `data/prepared/*/*.csv` contains `order_id`, `accepted_date`, these 13 features, and the target. It removes all other raw metadata.

Policy scenarios additionally include missing/expired authorization and unknown destinations. Those scenarios are not completed historical orders and must not enter the lead-time training table.

## How the synthetic generator works

Delivery combines supplier handling, route allowance, stock shortfall and replenishment, backlog, condition and seasonal effects. It adds random variation and occasional unobservable disruption delays. The supplier quote is a noisy estimate known before the future outcome. Aircraft model itself has no direct causal delivery effect in this starter.

This is intentionally learnable. Students must not copy the generator's hidden outcome formula as their prediction algorithm. Record which inputs improve validation error. The dataset contains clean, complete inputs. The model has missing-value handling, but that capability is not evidence that it performs well on messy operational records.

The approved training derivative is a fictional teaching release. Removing a classification field alone is **not** authorization to release real restricted information. See the policy guide before publishing another dataset.
