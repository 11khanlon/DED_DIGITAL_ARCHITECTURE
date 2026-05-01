#%%
import os
import sys
import numpy as np
import pandas as pd
import re
#%%
# IMPORT CLEANING FUNCTION
sys.path.append(
    r"C:\Users\Kayleigh\DIGITAL_ARCH_REPO\RPMI_DATA_DEV\ontology_development\ontology_iteration2"
)
from ingestion.clean_data import clean_columns

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

# SYSTEM INFERENCE
def extract_system(col):

    c = normalize(col)

    if "pf1" in c: return "PF1"
    if "pf2" in c: return "PF2"
    if "pf3" in c: return "PF3"
    if "pf4" in c: return "PF4"

    if "center purge" in c: return "CP1"


    if (
    "laser" in c or 
    "fiber" in c or 
    "beam" in c or 
    "di water" in c or 
    "power from meter" in c or
    "alps" in c or
    "optics" in c
    ):
        return "LASER_01"
    
    if "pos" in c or "velocity" in c or "head temp" in c or "layer" in c:
        return "MH1"

    if "camera" in c or "melt pool" in c: return "CAM_01"

    if "o2 sensor" in c: return "O2_SENSOR"
    if "h2o sensor" in c: return "H2O_SENSOR"

    if "pressure" in c:
        return "RPMI_01"
    
    if "toolcode" in c:
        return "PROCESS_CONTROLLER"

    return "RPMI_01"


def classify_state_variable(c):

    if "warning" in c:
        return ("WARNING_FLAG", c)

    if "alarm" in c:
        return ("ALARM_FLAG", c)

    if "enabled" in c:
        return ("STATE_ENABLED", c)

    if "low level" in c:
        return ("LOW_THRESHOLD", c)

    if "high level" in c:
        return ("HIGH_THRESHOLD", c)

    return None

# PARAMETER MAPPING (FULL COVERAGE + DEBUG)
def make_parameter_id(col):

    c = normalize(col)

    # ---------------- TIME ----------------
    if "timestamp" in c:
        return None

    # ---------------- MOTION ----------------
    if "pos x" in c: return "POSITION_X"
    if "pos y" in c: return "POSITION_Y"
    if "pos z" in c: return "POSITION_Z"

    if "velocity x" in c: return "VELOCITY_X"
    if "velocity y" in c: return "VELOCITY_Y"
    if "velocity z" in c: return "VELOCITY_Z"

    if "motion compensation" in c:
        return "MOTION_COMPENSATION_ACTIVE"

    if "alps spot size" in c:
        return "SPOT_SIZE"
    
    # STATE OVERRIDE (IMPORTANT)
    state = classify_state_variable(c)
    if state:
        param_id, scope = state
        return param_id, scope
   
    # LASER DIAGNOSTICS / OPTICAL METROLOGY MODULE
    if "feed fiber" in c:
        return "LASER_FEED_FIBER_SIGNAL"

    if "process fiber" in c:
        return "LASER_PROCESS_FIBER_SIGNAL"

    if "beam flags" in c:
        return "LASER_BEAM_FLAGS"

    if "ffbd" in c:
        return "FIBER_BACKSCATTER_SIGNAL"
    
    if "toolcode execution time" in c:
        return "TOOLCODE_EXECUTION_TIME"
    
    if "alps" in c:
        return "OPTICAL_ALIGNMENT_POSITION"
    

    # ---------------- POWDER FEEDERS ----------------
    if "powder low" in c:
        return "POWDER_LOW_FLAG"
    for pf in ["pf1", "pf2", "pf3", "pf4"]:
        if pf in c and "rpm setpoint" in c:
            return f"RPM_SETPOINT_{pf.upper()}"
        if pf in c and "rpm" in c:
            return f"RPM_{pf.upper()}"
        if pf in c and "mflow" in c:
            return f"ARGON_MFLOW_{pf.upper()}"
        if pf in c and "vflow" in c:
            return f"ARGON_VFLOW_{pf.upper()}"
        if pf in c and "temp" in c:
            return f"ARGON_TEMP_{pf.upper()}"
        if pf in c and "pressure" in c:
            return f"ARGON_PRESSURE_{pf.upper()}"
       

    # ---------------- CENTER PURGE ----------------
    if "center purge" in c and "mflow" in c:
        return "ARGON_MFLOW_CP1"
    if "center purge" in c and "vflow" in c:
        return "ARGON_VFLOW_CP1"
    if "center purge" in c and "temp" in c:
        return "ARGON_TEMP_CP1"
    if "center purge" in c and "pressure" in c:
        return "ARGON_PRESSURE_CP1"

    # ---------------- LASER ----------------
    if "laser power" in c: return "LASER_POWER"
    if "laser setpoint" in c: return "LASER_POWER_SETPOINT"
    if "laser on" in c: return "LASER_ON"
    if "laser water flow" in c: return "LASER_COOLING_FLOW"
    if "laser water temp" in c: return "LASER_COOLING_TEMP"

    # ---------------- GAS ----------------
    if "o2 sensor" in c: return "OXYGEN_SENSOR"
    if "h2o sensor" in c: return "HUMIDITY_SENSOR"

    # ---------------- THERMAL ----------------
    if "head temperature" in c: return "HEAD_TEMPERATURE"
    if "camera temp" in c: return "CAMERA_TEMPERATURE"
    if "di water temp" in c: return "DI_WATER_TEMP"

    # ---------------- PRESSURE ----------------
    if "box pressure" in c: return "BOX_PRESSURE"
    if "dust collector" in c: return "DUST_COLLECTOR_PRESSURE"
    if "manifold pressure" in c: return "MANIFOLD_PRESSURE"

    # ---------------- BUILD ----------------
    if "layer" in c: return "LAYER_ID"
    if "path setpoint velocity" in c: return "SCAN_SPEED"

    # ---------------- VISION ----------------
    if "melt pool area" in c: return "MELT_POOL_AREA"

    # ---------------- METROLOGY ----------------
    if "beam size" in c: return "BEAM_SIZE"
    if "beam pos x" in c: return "BEAM_POS_X"
    if "beam pos y" in c: return "BEAM_POS_Y"
    if "power from meter" in c: return "LASER_POWER_METER"

    return None


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
                "timestamp": timestamp,
                "system_id": system_id,
                "parameter_id": param_id,
                "state_scope": state_scope,
                "value": val,
                "unit": extract_unit(col)
            })
            process_parameters.append({
                "parameter_id": param_id,
                "description": val,
                "unit": extract_unit(col)
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

