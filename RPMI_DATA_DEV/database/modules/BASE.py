#%%
import pandas as pd

#%%
'''
work, organization, and measurement

'''

def build_base_module():

    organization = pd.DataFrame({
        "organization_id": ["ORG_001"],
        "organization_name": ["RPMI Lab"],
        "organization_type": ["research_lab"],
        "location": ["USA"]
    })

    person = pd.DataFrame({
        "person_id": ["P001", "P002"],
        "first_name": ["Kayleigh", "Operator_A"],
        "last_name": ["Hanlon", "Smith"],
        "role": ["engineer", "technician"],
        "organization_id": ["ORG_001", "ORG_001"]
    })

    qualification = pd.DataFrame({
        "qualification_id": ["Q001", "Q002"],
        "person_id": ["P001", "P002"],
        "qualification_type": ["welding_cert", "data_systems_cert"],
        "qualification_level": ["level_2", "level_1"]
    })


    return {
        "organization": organization,
        "person": person,
        "qualification": qualification,
        
    }


