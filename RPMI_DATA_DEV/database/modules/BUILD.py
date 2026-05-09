import numpy as np 
import pandas as pd 
import sys
sys.path.append("C:/Users/Kayleigh/DIGITAL_ARCH_REPO/RPMI_DATA_DEV/ontology_development/ontology_iteration2")
from RPMI_DATA_DEV.ingestion.parameter_inputs import toolpath_parameters

'''
this is print_metadata
printparameters, printwarnings, printevents, printstatus
layer count, speed

execution context links everything together 
''' 


#%% vocabulary layer 
def create_build_module(tic_observations):

    build_df = pd.DataFrame({
        "build_id": ["BUILD_001"],
        "machine_id": ["RPMI_01"],
        "material_id": ["MAT_IN718_01"],
        "process_id": ["PROC_001"],
        "base_id": ["BASE_001"],

        # derive from data (good ✔)
        "start_time": [tic_observations["timestamp"].min()],
        "end_time": [tic_observations["timestamp"].max()],

        "status": ["completed"]
    })

    return build_df



#creating parameters for later 
def create_build_parameters(tic_observations, thermocouple_observations):

    # ---------------- MACHINE PARAMETERS (SETPOINTS) ----------------
    machine_params = toolpath_parameters.copy()

    machine_params["build_id"] = "BUILD_001"
    machine_params["source"] = "machine_setpoint"

    machine_params = machine_params.rename(columns={
        "value": "target_value"
    })

    machine_params = machine_params[[
        "build_id",
        "parameter_id",
        "target_value",
        "unit",
        "source"
    ]]


    # ---------------- TIC PARAMETERS (OBSERVED PROCESS) ----------------
    tic_params = (
        tic_observations[[
            "build_id",
            "parameter_id",
            "value",
            "unit"
        ]]
        .dropna()
        .drop_duplicates()
        .copy()
    )

    tic_params["source"] = "machine_observation"


    # ---------------- SENSOR PARAMETERS (THERMOCOUPLE) ----------------
    sensor_params = (
        thermocouple_observations[[
            "build_id",
            "parameter_id",
            "value",
            "unit"
        ]]
        .dropna()
        .drop_duplicates()
        .copy()
    )

    sensor_params["source"] = "sensor_observation"


    # ---------------- COMBINE ALL ----------------
    build_parameters = pd.concat(
        [machine_params, tic_params, sensor_params],
        ignore_index=True,
        sort=False
    )

    return build_parameters

