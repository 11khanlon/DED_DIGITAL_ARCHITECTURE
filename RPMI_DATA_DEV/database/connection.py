from sqlalchemy import create_engine
import pandas as pd
import uuid
import sys
import numpy as np


DB_USER = "postgres"
DB_PASSWORD = "password"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "am_cdm"

engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)


tic_rows = []

for _, row in tic_df.iterrows():

    tic_rows.append({

        "event_id": str(uuid.uuid4()),

        "build_id": row["build_id"],

        "system_id": row["system_id"],

        "parameter_id": row["parameter_id"],

        "timestamp_utc": row["timestamp"],

        "value_numeric": row["value"],

        "quality_flag": "GOOD"
    })

tic_sql_df = pd.DataFrame(tic_rows)

tic_sql_df.to_sql(
    "TICEvent",
    engine,
    if_exists="append",
    index=False
)
