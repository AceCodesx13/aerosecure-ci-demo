"""Single source of truth for the starter dataset and model inputs."""
VERSION = '1.0.0'
SEED = 20261012
LABELS = ['Unrestricted', 'Restricted', 'Highly Restricted']
CATEGORICAL = ['aircraft_model_id', 'part_category_id', 'supplier_id', 'condition', 'origin_region_id', 'destination_region_id']
NUMERIC = ['quantity_ordered', 'stock_at_acceptance', 'supplier_backlog_days', 'quoted_lead_time_days', 'route_transit_days', 'route_customs_days', 'order_month']
FEATURES = CATEGORICAL + NUMERIC
TARGET = 'actual_delivery_days'
PREPARED_COLUMNS = ['order_id', 'accepted_date'] + FEATURES + [TARGET]
TRAIN_CUTOFF = '2025-01-01'
VALIDATION_CUTOFF = '2025-05-01'
OBSERVATION_END = '2026-09-30'
