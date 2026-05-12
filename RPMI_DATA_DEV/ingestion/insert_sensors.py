import numpy as np 
import pandas as pd 
import sys
from RPMI_DATA_DEV.database.connection import engine
sys.path.append("C:/Users/Kayleigh/DIGITAL_ARCH_REPO/RPMI_DATA_DEV")
from ingestion.parameter_inputs import toolpath_parameters


def split_value(val):
    if isinstance(val, (int, float, np.number)):
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

    build_param_df.to_sql(
        "BuildParameter",
        engine,
        if_exists="append",
        index=False
    )

    return build_param_df