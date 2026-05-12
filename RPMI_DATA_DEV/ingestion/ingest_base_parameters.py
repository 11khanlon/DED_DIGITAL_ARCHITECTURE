import pandas as pd
import sys
sys.path.append("C:\\Users\\Kayleigh\\DIGITAL_ARCH_REPO\\RPMI_DATA_DEV")
from database.connection import engine


# =========================================================
# BUILD BASE MODULE
# =========================================================
def build_base_module():

    organization = pd.DataFrame([
        {
            "organization_id": "ORG_001",
            "organization_name": "RPMI Lab",
            "organization_type": "research_lab",
            "location": "USA"
        }
    ])

    person = pd.DataFrame([
        {
            "person_id": "P001",
            "first_name": "Kayleigh",
            "last_name": "Hanlon",
            "role": "engineer",
            "organization_id": "ORG_001"
        },
        {
            "person_id": "P002",
            "first_name": "Operator_A",
            "last_name": "Smith",
            "role": "technician",
            "organization_id": "ORG_001"
        }
    ])

    qualification = pd.DataFrame([
        {
            "qualification_id": "Q001",
            "person_id": "P001",
            "qualification_type": "welding_cert",
            "qualification_level": "level_2"
        },
        {
            "qualification_id": "Q002",
            "person_id": "P002",
            "qualification_type": "data_systems_cert",
            "qualification_level": "level_1"
        }
    ])

    return organization, person, qualification


# =========================================================
# INGEST TO POSTGRES
# =========================================================
def ingest_base_module():

    organization, person, qualification = build_base_module()

    print("\n===================================")
    print("INSERTING BASE SAM MODULE")
    print("===================================\n")

    # ---------------- ORGANIZATION ----------------
    organization.to_sql(
        "Organization",
        engine,
        if_exists="append",
        index=False
    )
    print("Inserted Organization")

    # ---------------- PERSON ----------------
    person.to_sql(
        "Person",
        engine,
        if_exists="append",
        index=False
    )
    print("Inserted Person")

    # ---------------- QUALIFICATION ----------------
    qualification.to_sql(
        "Qualification",
        engine,
        if_exists="append",
        index=False
    )
    print("Inserted Qualification")

    print("\nDONE: SAM BASE MODULE INGESTED")

    return {
        "organization": organization,
        "person": person,
        "qualification": qualification
    }


# =========================================================
# RUN
# =========================================================
if __name__ == "__main__":
    ingest_base_module()