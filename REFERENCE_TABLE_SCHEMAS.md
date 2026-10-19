# Reference table schemas
These tables accompany the order dictionary in `02_DATA_GUIDE.md`. Values are fictional unless specifically identified as real aircraft model names.

## aircraft_models.csv
20 rows.

| Column | Example value |
|---|---|
| `aircraft_model_id` | AC-01 |
| `manufacturer` | Airbus |
| `model` | A220-100 |
| `aircraft_category` | Small single-aisle jet |
| `compatibility_scope` | Illustrative classroom associations only |

## aircraft_parts.csv
400 rows.

| Column | Example value |
|---|---|
| `aircraft_part_id` | AC-01-PC-01 |
| `aircraft_model_id` | AC-01 |
| `part_category_id` | PC-01 |
| `part_number` | SIM-AC-01-PC-01 |
| `association_status` | Illustrative, not verified aircraft compatibility |

## part_categories.csv
20 rows.

| Column | Example value |
|---|---|
| `part_category_id` | PC-01 |
| `part_category` | Engine oil filter |
| `part_group` | Consumable |
| `simulated_base_days` | 5 |
| `allowed_conditions` | New |

## regions.csv
3 rows.

| Column | Example value |
|---|---|
| `region_id` | REG-A |
| `name` | Fictional Region A |
| `real_geographic_mapping` | None |

## routes.csv
9 rows.

| Column | Example value |
|---|---|
| `origin_region_id` | REG-A |
| `destination_region_id` | REG-A |
| `route_transit_days` | 2 |
| `route_customs_days` | 0 |

## shipment_policy.csv
9 rows.

| Column | Example value |
|---|---|
| `shipment_restriction_classification` | Unrestricted |
| `destination_region_id` | REG-A |
| `destination_eligible` | True |
| `requirement` | None |

## supplier_eligibility.csv
60 rows.

| Column | Example value |
|---|---|
| `supplier_id` | SUP-A |
| `part_category_id` | PC-01 |
| `allowed_conditions` | New |

## suppliers.csv
9 rows.

| Column | Example value |
|---|---|
| `supplier_id` | SUP-A |
| `name` | Aster Consumables |
| `origin_region_id` | REG-A |
| `specialty_group` | Consumable |
| `simulated_handling_days` | 2 |
| `simulated_replenishment_factor` | 0.7 |
