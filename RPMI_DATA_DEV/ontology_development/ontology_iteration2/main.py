import os
import numpy as np
import pandas as pd

from ingestion.clean_data import clean_columns
from mapping.parameter_map import convert_to_tic
from modules.TIC import build_tic_observations
from modules.PROCESS import build_process_module

# ---------------- LOAD ----------------
os.chdir(r"C:\Users\Kayleigh\DIGITAL_ARCH_REPO\RPMI_DATA_DEV\data_csv_examples")
df = pd.read_csv("dlog_2023-08-09_1106_purge_testing.csv", low_memory=False)

#---------------- CLEAN ----------------
parameter_table, cleaned_df = clean_columns(df)


#---------------- PARAMETER MAPPING ----------------
tic_df, process_parameters = convert_to_tic(cleaned_df)


#---------------- ASSEMBLE MODULES ----------------
tic_observations = build_tic_observations(tic_df)
process_df = build_process_module(tic_df)

print(process_df)
