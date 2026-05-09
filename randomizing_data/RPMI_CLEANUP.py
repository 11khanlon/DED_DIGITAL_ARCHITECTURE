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

#%% --- Load data ---
os.chdir(r"C:\Users\Kayleigh\DIGITAL_ARCH_REPO\RPMI_DATA_DEV\data_csv_examples")

df = pd.read_csv("dlog_2023-08-09_1106_purge_testing.csv", low_memory=False)

#%% --- STEP 1: Clean column names (MUST BE FIRST) ---
df.columns = (
    df.columns
    .str.strip()
    .str.replace('\ufeff', '', regex=False)
)

print("Columns:", df.columns.tolist())

# Ensure required columns exist
required_cols = ["TimeStamp"]
for col in required_cols:
    if col not in df.columns:
        raise ValueError(f"Missing column: {col}\nAvailable: {df.columns.tolist()}")

#%% --- STEP 2: Convert TimeStamp early ---
df["TimeStamp"] = pd.to_datetime(
    df["TimeStamp"],
    format="%Y-%m-%d %H:%M:%S",
    errors="coerce"
)

# Drop bad timestamps early (prevents downstream errors)
df = df.dropna(subset=["TimeStamp"]).reset_index(drop=True)

# Optional: add timezone
df["TimeStamp"] = df["TimeStamp"].dt.tz_localize("UTC")

#%% --- STEP 3: Track original shape ---
original_shape = df.shape

#%% --- STEP 4: Drop mostly empty columns ---
threshold = 0.8
fraction_nan_or_zero = df.apply(lambda col: ((col.isna()) | (col == 0)).mean())
df = df.drop(columns=fraction_nan_or_zero[fraction_nan_or_zero > threshold].index)

#%% --- STEP 5: Handle A2–A6 columns ---
cols_to_export = ['A2', 'A3', 'A4', 'A5', 'A6']
cols_exist = [c for c in cols_to_export if c in df.columns]

if cols_exist:
    df_export = df[['TimeStamp'] + cols_exist].copy()

    # Drop rows where all A2–A6 are empty/zero
    non_ts_cols_exp = [c for c in df_export.columns if c != 'TimeStamp']
    df_export = df_export[
        ~((df_export[non_ts_cols_exp].isna()) | (df_export[non_ts_cols_exp] == 0)).all(axis=1)
    ]

    df_export = df_export.reset_index(drop=True)
    df_export.to_csv("exported_A2_A6.csv", index=False)

    # Remove from main df
    df = df.drop(columns=cols_exist)

#%% --- STEP 6: Remove empty rows (but keep TimeStamp safe) ---
non_ts_cols = [c for c in df.columns if c != 'TimeStamp']

df = df[
    ~((df[non_ts_cols].isna()) | (df[non_ts_cols] == 0)).all(axis=1)
]

df = df.reset_index(drop=True)

#%% --- STEP 7: Save cleaned dataset ---
df.to_csv("cleaned_original.csv", index=False)

# Save column names
pd.DataFrame(df.columns, columns=["Variable_Names"]).to_csv(
    "cleaned_variable_names.csv", index=False
)

#%% --- STEP 8: Summary ---
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


#%%

'''need to add timestamp, set to UTC. timestamp once the folder is available. 
If available and the laser is on, create a string saying Good to start reading, then create a timestamp. 
When the laser is turned off - check laser on time - then timestamp the folder that process has ended 
Maybe, we do not need to cleanup the rows for later?'''

#Create laser on time stamp function, event = LaserOn
def find_laser_timeframe(df):

    #pd.to_datetime(...), converts strings into real datetime objects. Can perform subtraction. errors = "coerce" will convert unparseable strings to NaT (Not a Time) 
    df["TimeStamp"] = pd.to_datetime(df["TimeStamp"], format="%Y-%m-%d %H:%M:%S", errors="coerce")  
    df = df.dropna(subset=["TimeStamp"]).reset_index(drop=True) #removes rows were TimeStamp is missing
    df["TimeStamp"] = df["TimeStamp"].dt.tz_convert("UTC")  # .dt access datetime proprties, UTC will attatch UTC timezone
    
    
    laser_on_indices = df.index[df["Laser On"] != 0]  # Find first index where Laser On is not zero

    if len(laser_on_indices) == 0:
        return None, 0     #if laser is never on, return None and 0 duration

    first_on_idx = laser_on_indices[0]

    if first_on_idx > 0:    
        reference_idx = first_on_idx - 1  #pick row just before laser turns on as a reference timestamp
    else:
        reference_idx = first_on_idx

    reference_timestamp = df.loc[reference_idx, "TimeStamp"]

    last_on_idx = laser_on_indices[-1]  # Find last index where Laser On is not zero
    final_timestamp = df.loc[last_on_idx, "TimeStamp"]

    laser_on_duration = final_timestamp - reference_timestamp
    laser_on_duration_seconds = laser_on_duration.total_seconds() 

    return reference_timestamp, laser_on_duration_seconds

reference_timestamp, laser_on_duration_seconds = find_laser_timeframe(df)
print(reference_timestamp, laser_on_duration_seconds)

