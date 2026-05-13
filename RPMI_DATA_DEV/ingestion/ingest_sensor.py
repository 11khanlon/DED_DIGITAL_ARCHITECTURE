import numpy as np 
import pandas as pd 
import sys
sys.path.append("C:\\Users\\Kayleigh\\DIGITAL_ARCH_REPO\\RPMI_DATA_DEV")
from database.connection import engine
csv_path = r"C:\\Users\\Kayleigh\\DIGITAL_ARCH_REPO\\RPMI_DATA_DEV\\data_csv_examples\\PYRAMID.csv"

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
def ingest_thermocouple_tic(
    csv_path,
    build_id="BUILD_001",
    table_name="thermocouple_tic"
):

    # -----------------------------------------------------
    # build dataframe
    # -----------------------------------------------------
    df = build_thermocouple_tic(
        csv_path=csv_path,
        build_id=build_id
    )

    # -----------------------------------------------------
    # ingest to postgres
    # -----------------------------------------------------
    df.to_sql(
        table_name,
        engine,
        if_exists="append",
        index=False,
        method="multi",
        chunksize=1000
    )

    print(f"Ingested {len(df)} rows into {table_name}")

    return df


# =========================================================
# EXAMPLE USAGE
# =========================================================

if __name__ == "__main__":


    ingest_thermocouple_tic(
        csv_path=csv_path,
        build_id="BUILD_001"
    )

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