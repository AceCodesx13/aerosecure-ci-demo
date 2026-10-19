"""Fictional classroom policy. This function does not enforce S3 access."""
from schema import LABELS

ROLE_CLEARANCE = {'student': 0, 'mentor': 1, 'administrator': 2}

def can_read(role, classification):
    return role in ROLE_CLEARANCE and classification in LABELS and ROLE_CLEARANCE[role] >= LABELS.index(classification)

def shipment_decision(classification, destination_eligible, authorization_status):
    if classification not in LABELS or destination_eligible is None:
        return 'Review required', 'Unknown classification or destination'
    if not destination_eligible:
        return 'Blocked', 'Destination is ineligible under the fictional policy'
    if classification == 'Unrestricted':
        return 'Allowed', 'Eligible destination, no special authorization required'
    if classification == 'Restricted' and authorization_status == 'Valid':
        return 'Allowed', 'Valid destination authorization'
    if classification == 'Highly Restricted' and authorization_status == 'Approved after review':
        return 'Allowed', 'Explicit human approval recorded'
    return 'Review required', 'Required authorization or review is missing, expired or incomplete'
