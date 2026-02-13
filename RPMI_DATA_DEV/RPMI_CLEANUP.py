import numpy as np 
import pandas as pd 
#import requests
import time
#import xmltodict
import json
import socket 
import sqlite3 
from datetime import datetime
import csv 
import os



#%%
# --- Load data and get column values ---
os.chdir(r"C:\Users\Kayleigh\DIGITAL_ARCH_REPO\RPMI_DATA_DEV")
df = pd.read_csv("dlog_2023-08-09_1106_purge testing.csv", low_memory=False)

#%%
# --- Get column names and Laser on timestamp ---
columns = df.columns 
column_names = df.columns.tolist()

'''need to add timestamp, set to UTC. timestamp once the folder is available. 
If available and the laser is on, create a string saying Good to start reading, then create a timestamp. 
When the laser is turned off - check laser on time - then timestamp the folder that process has ended 
Maybe, we do not need to cleanup the rows for later?'''


#Create laser on time stamp function 
def find_laser_timeframe(df):
    df["TimeStamp"] = pd.to_datetime(df["TimeStamp"], errors="coerce")
    df["TimeStamp"] = df["TimeStamp"].dt.tz_localize("UTC")
    
    # Find first index where Laser On is not zero
    laser_on_indices = df.index[df["Laser On"] != 0]

    if len(laser_on_indices) == 0:
        return None, 0

    first_on_idx = laser_on_indices[0]

    if first_on_idx > 0:
        reference_idx = first_on_idx - 1
    else:
        reference_idx = first_on_idx

    reference_timestamp = df.loc[reference_idx, "TimeStamp"]

    last_on_idx = laser_on_indices[-1]
    final_timestamp = df.loc[last_on_idx, "TimeStamp"]

    laser_on_duration = final_timestamp - reference_timestamp
    laser_on_duration_seconds = laser_on_duration.total_seconds() 
    return reference_timestamp, laser_on_duration_seconds
#%%

#run this if there is missing data -- for now I do not know if there will be 

# --- Track original shape ---
original_shape = df.shape

#  Drop columns that are mostly NaN or 0 ---
threshold = 0.8  # 80% cutoff
fraction_nan_or_zero = df.apply(lambda col: ((col.isna()) | (col == 0)).mean())
df = df.drop(columns=fraction_nan_or_zero[fraction_nan_or_zero > threshold].index)

#  Identify A2–A6 columns that exist in the current df ---
cols_to_export = ['A2', 'A3', 'A4', 'A5', 'A6']
cols_exist = [c for c in cols_to_export if c in df.columns]

# Export A2–A6 to new file (keep same header names) ---
if cols_exist:
    df_export = df[['TimeStamp'] + cols_exist].copy()

    # Drop completely blank rows in export (including NaN or all zeros)
    non_ts_cols_exp = [c for c in df_export.columns if c != 'TimeStamp']
    df_export = df_export[~((df_export[non_ts_cols_exp].isna() | (df_export[non_ts_cols_exp] == 0)).all(axis=1))]

    # Remove blank timestamps
    df_export = df_export[df_export['TimeStamp'].notna() & (df_export['TimeStamp'] != '')]

    # Reset index and export
    df_export = df_export.reset_index(drop=True)
    df_export.to_csv("exported_A2_A6.csv", index=False)

    # Remove A2–A6 from main DataFrame
    df = df.drop(columns=cols_exist)

#  Remove rows where Timestamp has no valid data ---
non_ts_cols = [c for c in df.columns if c != 'TimeStamp']

# Drop if all non-Timestamp columns are NaN or 0
df = df[~((df[non_ts_cols].isna() | (df[non_ts_cols] == 0)).all(axis=1))]

# Drop if Timestamp itself is missing or blank
df = df[df['TimeStamp'].notna() & (df['TimeStamp'] != '')]

# Reset index so rows "move up" cleanly ---
df = df.reset_index(drop=True)

#  Save cleaned dataset ---
df.to_csv("cleaned_original.csv", index=False)

# Save variable (column) names that remain ---
cleaned_columns = pd.DataFrame(df.columns, columns=["Variable_Names"])
cleaned_columns.to_csv("cleaned_variable_names.csv", index=False)

# Print and save summary ---
cleaned_shape = df.shape
summary = (
    f"Original file shape: {original_shape[0]} rows, {original_shape[1]} columns\n"
    f"Cleaned file shape:  {cleaned_shape[0]} rows, {cleaned_shape[1]} columns\n"
    f"Columns removed:     {original_shape[1] - cleaned_shape[1]}\n"
    f"Rows removed:        {original_shape[0] - cleaned_shape[0]}\n"
    f"A2–A6 exported columns: {', '.join(cols_exist) if cols_exist else 'None found'}\n"
)
print(summary)

with open("cleanup_summary.txt", "w") as f:
    f.write(summary)