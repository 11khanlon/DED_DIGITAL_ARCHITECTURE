import numpy as np 
import pandas as pd


'''
BASE MODULE
person, organization, and measurement

static ontology 
'''

person = pd.DataFrame({
    "person_id": ["P001", "P002"],
    "person_first_name": ["Kayleigh", "Operator_A"],
    "person_last_name": ["Hanlon", "Smith"],
    "person_role": ["engineer", "technician"],
    "organization_id": ["ORG_001", "ORG_001"]
})

organization = pd.DataFrame({
    "organization_id": ["ORG_001"],
    "organization_name": ["RPMI Lab"],
    "organization_type": ["research_lab"],
    "location": ["USA"]
})

qualification = pd.DataFrame({
    "qualification_id": ["Q001", "Q002"],
    "qualification_type": ["welding_cert", "data_systems_cert"],
    "qualification_level": ["level_2", "level_1"],
    "qualifying_organization": ["AWS", "internal_training"],
    "person_id": ["P001", "P002"]
})

measurement = pd.DataFrame({
    "measurement_id": [],

    "value": [],
    "unit": [],

    "data_type": [],

    "timestamp": [],

    "uncertainty": [],
    "calibration_id": [],

    "is_valid": [],

    "source_system": [],
    "source_parameter": [],

    "build_id": []
})