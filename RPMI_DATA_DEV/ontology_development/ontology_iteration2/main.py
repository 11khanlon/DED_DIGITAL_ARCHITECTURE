import os
import numpy as np
import pandas as pd

from ingestion.clean_data import clean_columns
from ingestion.events import get_laser_start_event


# ---------------- LOAD ----------------
os.chdir(r"C:\Users\Kayleigh\DIGITAL_ARCH_REPO\RPMI_DATA_DEV\data_csv_examples")
df = pd.read_csv("dlog_2023-08-09_1106_purge_testing.csv", low_memory=False)

#---------------- CLEAN ----------------
parameter_table, cleaned_df = clean_columns(df)


print(parameter_table, cleaned_df)
