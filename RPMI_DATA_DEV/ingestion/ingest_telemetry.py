#%%
'''
Telemetry is the measurement and transmission of data from a system 
what is the machine doing and what values are being measured?

semantic telemetry ingestion pipeline

'''
#%%
from unittest import result

import pandas as pd
import sys 
import os 
import re 
import uuid 
import numpy as np 

sys.path.append(
    r"C:\\Users\\Kayleigh\\DIGITAL_ARCH_REPO\\RPMI_DATA_DEV"
)
from ingestion.clean_data import clean_columns
from ingestion.ontology_mapper import map_parameter
from database.connection import engine

#%%
# --------- LOAD RPMI MACHINE DATA ------------
os.chdir(r"C:\\Users\\Kayleigh\\DIGITAL_ARCH_REPO\\RPMI_DATA_DEV\\data_csv_examples")
df = pd.read_csv("dlog_2023-08-09_1106_purge_testing.csv", low_memory=False)


#%%
#Extract Unit
def extract_unit(col):
    match = re.search(r"\((.*?)\)", col)
    if match:
        return match.group(1)
    return None

#%%
# NORMALIZATION
def normalize(col):
    col = col.lower().strip()
    col = re.sub(r"[^a-z0-9 ]", " ", col)
    col = re.sub(r"\s+", " ", col)
    return col

parameter_table, df = clean_columns(df)


#%%
# TIC CONVERSION (PRINT EVERYTHING)
def convert_to_tic(df):

    # STORAGE CONTAINERS
    records = []
    parameter_rows = []
    system_rows = []
    mapped = []
    unmapped = []


    # TIC CONVERSION START
    print("\n============================================")
    print("STARTING TELEMETRY INGESTION")
    print("============================================\n")

    # COLUMN LOOP - FINDING VARIABLE NAMES

    for col in df.columns:

        # Skip timestamp column
        if col == "TimeStamp":
            continue

        print("\n-------------------------------------")
        print("RAW COLUMN:", col)
      
        # Normalize variable name
        normalized_col = normalize(col)
        print("NORMALIZED:", normalized_col)

      
        # Extract unit
        extracted_unit = extract_unit(col)
        print("EXTRACTED UNIT:", extracted_unit)

        # Semantic ontology mapping
        mapping = map_parameter(normalized_col)

        # Unmapped variables
        if mapping is None:

            print("STATUS: UNMAPPED")

            unmapped.append(col)

            continue

       
        # Mapping results
        parameter_id = mapping["parameter_id"]

        parameter_name = mapping["parameter_name"]

        parameter_type = mapping["parameter_type"]

        system_id = mapping["system_id"]

        data_type = mapping["data_type"]

        mapped.append(col)

        print("STATUS: MAPPED")
        print("PARAMETER:", parameter_id)
        print("SYSTEM:", system_id)


        # PARAMETER TABLE ENTRY
        parameter_rows.append({

            "parameter_id": parameter_id,

            "parameter_name": parameter_name,

            "parameter_type": parameter_type,

            # prefer CSV extracted unit if available
            "unit": extracted_unit if extracted_unit else mapping["unit"],

            "physical_meaning": None,

            "data_type": data_type
        })

        # SYSTEM TABLE ENTRY
        system_rows.append({

            "system_id": system_id,

            "machine_id": "RPMI_MACHINE_01",

            "parent_system_id": None,

            "system_name": system_id,

            "system_type": "TelemetrySubsystem",

            "manufacturer": "RPMI"
        })

     
        # ROW LOOP → GENERATE TIC EVENTS
        for i, row in df.iterrows():

            val = row[col]

            timestamp = row["TimeStamp"]

            # Skip empty values
            if pd.isna(val):
                continue

            if isinstance(val, str) and val.strip() == "":
                continue

            # Numeric vs text handling
            numeric_val = None

            text_val = None

            if isinstance(
                val,
                (int, float, np.integer, np.floating)
            ):

                numeric_val = float(val)

            else:

                text_val = str(val)

            # Debug preview
            if i < 2:

                print(
                    f"row[{i}] "
                    f"ts={timestamp} "
                    f"value={val}"
                )

            
            # TIC EVENT RECORD
            records.append({

                "event_id": str(uuid.uuid4()),

                "build_id": "BUILD_001",

                "system_id": system_id,

                "parameter_id": parameter_id,

                "timestamp_utc": timestamp,

                "x_coord": None,

                "y_coord": None,

                "z_coord": None,

                "layer_number": None,

                "value_numeric": numeric_val,

                "value_text": text_val,

                "quality_flag": "GOOD",

                "state_scope": None
            })


 
    # BUILD DATAFRAMES

    tic_df = pd.DataFrame(records)

    parameter_df = (
        pd.DataFrame(parameter_rows)
        .drop_duplicates(subset=["parameter_id"])
    )

    system_df = (
        pd.DataFrame(system_rows)
        .drop_duplicates(subset=["system_id"])
    )

    unmapped_df = pd.DataFrame(unmapped, columns=["unmapped_column"])

    # SUMMARY

    print("\n============================================")
    print("INGESTION SUMMARY")
    print("============================================\n")

    print("TOTAL TELEMETRY VARIABLES:", len(df.columns) - 1)

    print("MAPPED VARIABLES:", len(mapped))

    print("UNMAPPED VARIABLES:", len(unmapped))

    print("\nUNMAPPED LIST:")

    for u in unmapped:
        print(" -", u)

    print("\nTOTAL TIC EVENTS:", len(tic_df))


    
    # INSERT INTO SQL

    print("\n============================================")
    print("INSERTING INTO POSTGRESQL")
    print("============================================\n")

    # INSERT SYSTEMS
    system_df.to_sql(
        "System",
        engine,
        if_exists="append",
        index=False
    )

    print("Inserted systems")


    # INSERT PARAMETERS
    parameter_df.to_sql(
        "Parameter",
        engine,
        if_exists="append",
        index=False
    )

    print("Inserted parameters")


  
    # INSERT TIC EVENT

    tic_df.to_sql(
        "TICEvent",
        engine,
        if_exists="append",
        index=False
    )

    print("Inserted TIC events")



    # COMPLETE
    print("\n============================================")
    print("TELEMETRY INGESTION COMPLETE")
    print("============================================")

    return {
    "tic_df": tic_df,
    "parameter_df": parameter_df,
    "system_df": system_df,
    "unmapped_df": unmapped_df
    }


result = convert_to_tic(df)
tic_df = result["tic_df"]

print(tic_df.head())
print(tic_df.columns)