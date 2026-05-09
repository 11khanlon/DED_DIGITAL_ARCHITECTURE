#%%
import numpy as np
import pandas as pd
import sys
import os

'''
What is observed/measured 
timestamped sensor data, position X, Y, Z, meltpool data, etc 
dynamic - TIC observations are not a static ontology model 

'''

#%%
def build_tic_observations(mapped_df, build_id="BUILD_001"):
    
    df = mapped_df.copy()

    # ---------------- ADD IDS ----------------
    df["observation_id"] = np.arange(len(df))
    df["build_id"] = build_id

    # ---------------- OPTIONAL METADATA ----------------
    df["measurement_error"] = None
    df["calibration_id"] = None
    df["sampling_rate_hz"] = 1
    df["sequence_index"] = df.groupby("parameter_id").cumcount()


    df["source_sensor"] = None
    df["missing_data_flag"] = None
    df["interpolation_method"] = None
    df["is_valid"] = None
    df["quality_score"] = None

    df["outlier_flag"] = None
    df["noise_level"] = None

    # ---------------- SELECT FINAL COLUMNS ----------------
    return df[
        [
            "observation_id",
            "build_id",
            "system_id",
            "parameter_id",
            "timestamp",
            "value",
            "unit",
            "measurement_error",
            "calibration_id",
            "sampling_rate_hz",
            "sequence_index",
            "source_system",
            "source_sensor",
        ]
    ]


def build_thermocouple_tic(csv_path, build_id="BUILD_001"):

    df = pd.read_csv(csv_path)

    # ----------------------------
    # reshape wide → long format
    # ----------------------------
    df_long = df.melt(
        id_vars=["timestamp"],
        value_vars=["ch0", "ch1", "ch2", "ch3"],
        var_name="channel_id",
        value_name="value"
    )

    # ----------------------------
    # add ontology fields
    # ----------------------------
    df_long["observation_id"] = np.arange(len(df_long))
    df_long["build_id"] = build_id
    df_long["system_id"] = "TC"
    df_long["parameter_id"] = "TEMPERATURE"
    df_long["unit"] = "°C"   # fix if your stream is °F
    df_long["response_time_ms"] = None
    df_long["location"] = "build_plate"


    thermocouple_observations = df_long[
        [
            "observation_id",
            "build_id",
            "system_id",
            "parameter_id",
            "channel_id",
            "timestamp",
            "value",
            "unit",
            "response_time_ms",
            "location"
        ]
    ]

    # reorder to match schema
    return thermocouple_observations



#%%


'''
Need to implement external sensor stream 

sensor_tic_metadata = pd.DataFrame({
    "system_id": [],
    "sensor_type": [],

    # optical-specific
    "resolution": [],
    "frame_rate": [],

    # thermal-specific
    "channel_id": [],

    # gas-specific
    "gas_type": [],

    # calibration
    "calibration_date": [],
    "drift_correction_factor": []
})


camera_tic = pd.DataFrame({
    "observation_id": [],
    "build_id": [],
    "system_id": ["CAM_01"],
    "parameter_id": ["MELT_POOL_AREA"],
    "timestamp": [],
    "value": [],  # float area

    # image-derived metadata
    "frame_id": [],
    "pixel_resolution": [],
    "exposure_time": [],
    "is_valid": []
})





gas_sensor_tic = pd.DataFrame({
    "observation_id": [],
    "build_id": [],
    "system_id": ["O2_SENSOR", "H2O_SENSOR"],
    "parameter_id": ["OXYGEN_PPM", "HUMIDITY_PPM"],

    "timestamp": [],
    "value": [],

    "unit": ["ppm"],

    # gas-specific metadata
    "flow_condition": [],
    "sampling_mode": ["continuous", "interval"],
})


motion_tic = pd.DataFrame({
    "observation_id": [],
    "build_id": [],
    "system_id": ["MH1"],

    "parameter_id": [
        "POSITION_X",
        "POSITION_Y",
        "POSITION_Z",
        "VELOCITY_X",
        "VELOCITY_Y",
        "VELOCITY_Z"
    ],

    "timestamp": [],
    "value": [],

    "unit": ["mm", "mm/s"],

    # motion metadata
    "frame_reference": [],
    "control_mode": ["open_loop", "closed_loop"]
})


tic_quality = pd.DataFrame({
    "observation_id": [],
    "build_id": [],

    "is_valid": [],
    "quality_score": [],

    "outlier_flag": [],
    "noise_level": [],

    "missing_data_flag": [],
    "interpolation_method": []
})

'''