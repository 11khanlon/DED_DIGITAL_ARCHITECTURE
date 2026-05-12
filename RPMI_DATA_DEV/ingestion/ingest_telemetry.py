import pandas as pd
import sys 
import os 
import re 


sys.path.append(
    r"C:\Users\Kayleigh\DIGITAL_ARCH_REPO\RPMI_DATA_DEV\ingestion"
)
from RPMI_DATA_DEV.ingestion.clean_data import clean_columns
from RPMI_DATA_DEV.ingestion.ontology_mapper import map_parameter

# --------- LOAD RPMI MACHINE DATA ------------
os.chdir(r"C:\Users\Kayleigh\DIGITAL_ARCH_REPO\RPMI_DATA_DEV\data_csv_examples")
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

# TIC CONVERSION (PRINT EVERYTHING)
def convert_to_tic(df):

    records = []
    unmapped = []
    mapped = []
    process_parameters = []

    print("\n================ TIC CONVERSION START ================\n")

    for col in df.columns:

        if col == "TimeStamp":
            continue

        param = make_parameter_id(col)

        if isinstance(param, tuple):
            param_id, state_scope = param
        else:
            param_id = param
            state_scope = None
        
        system_id = extract_system(col)

        # PRINT MAPPING INFO
        print("\n----------------------------------------")
        print("COLUMN:", col)
        print("SYSTEM:", system_id)
        print("PARAMETER:", param_id)

        if param_id is None:
            unmapped.append(col)
            param_id = f"UNMAPPED_{col}"
            print("STATUS: UNMAPPED")
        else:
            mapped.append(col)
            print("STATUS:  MAPPED")

        # ROW LOOP
        for i, row in df.iterrows():

            val = row[col]
            timestamp = row["TimeStamp"]

            if pd.isna(val):
                continue

            if isinstance(val, str) and val.strip() == "":
                continue
            
            if i < 2:  # ONLY PRINT FIRST 2 ROWS PER COLUMN (prevents spam)
                print(f"  row[{i}] → ts={timestamp}, val={val}")

            records.append({
                "build_id": "BUILD_001",
                "timestamp": timestamp,
                "system_id": system_id,
                "parameter_id": param_id,
                "state_scope": state_scope,
                "value": val,
                "unit": extract_unit(col)
        
            })
            process_parameters.append({
                "parameter_id": param_id,
            })

    # FINAL SUMMARY PRINT
    # =========================
    tic_df = pd.DataFrame(records)
    process_parameters = pd.DataFrame(process_parameters)   
    

    print("\n================ SUMMARY ================\n")
    print("Total columns:", len(df.columns) - 1)
    print("Mapped:", len(mapped))
    print("Unmapped:", len(unmapped))

    print("\nUNMAPPED VARIABLES:")
    for u in unmapped:
        print(" -", u)

    print("\n================ TIC OUTPUT PREVIEW ================\n")

    print(tic_df.head(20))
    print("\nTOTAL TIC ROWS:", len(tic_df))


    return tic_df, process_parameters
