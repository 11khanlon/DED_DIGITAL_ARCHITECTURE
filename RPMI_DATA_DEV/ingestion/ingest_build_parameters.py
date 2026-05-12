import numpy as np 
import pandas as pd 
import sys
sys.path.append("C:\\Users\\Kayleigh\\DIGITAL_ARCH_REPO\\RPMI_DATA_DEV")
from database.connection import engine
from ingestion.parameter_inputs import toolpath_parameters


def split_value(val):
    if pd.isna(val):
        return None, None

    if isinstance(val, (int, float, np.integer, np.floating)):
        return float(val), None
    else:
        return None, str(val)


def ingest_build_parameters(df, build_id):

    records = []

    for _, row in df.iterrows():

        num, text = split_value(row["value"])

        records.append({
            "build_id": build_id,
            "parameter_id": row["parameter_id"],
            "value_numeric": num,
            "value_text": text,
            "unit": row["unit"],
            "description": row["description"],
            "source": "toolpath_parameters"
        })

    build_param_df = pd.DataFrame(records)

    print(build_param_df.head())
    print("ROWS:", len(build_param_df))

    build_param_df.to_sql(
        "BuildParameter",
        engine,
        if_exists="replace",   # switch to append AFTER testing
        index=False
    )

    print("INSERT COMPLETE")

    return build_param_df


build_param_df = ingest_build_parameters(
    toolpath_parameters,
    build_id="BUILD_001"
)