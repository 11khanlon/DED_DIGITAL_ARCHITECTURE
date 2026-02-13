#%%
import numpy as np 
import pandas as pd 
import time
from datetime import datetime
import csv 
import os 

os.chdir(r"C:\Users\Kayleigh\DIGITAL_ARCH_REPO\RPMI_DATA_DEV")
df = pd.read_csv("dlog_2023-08-09_1106_purge testing.csv", low_memory=False)

#%%

"create random data from parameters from the rpmi. Also generate random material data"
" Make them realistic with parameters that I have found from literature "

rng = np.random.default_rng(seed=42) 
#seed = 42 you always get the same the random sequence, seed = 7 you get a different repeatable sequence


# --- Get column names and Laser on timestamp ---
columns = df.columns 
column_names1 = df.columns.tolist()
column_names = pd.Series(df.columns)
column_names.to_csv("RPMI_column_names.csv", index=False, header=False)

#%%

#Create laser on time stamp function 
def find_laser_timeframe(df):

    df["TimeStamp"] = pd.to_datetime(df["TimeStamp"], format="%Y-%m-%d %H:%M:%S", errors="coerce")  #pd.to_datetime(...), converts strings into real datetime objects
    df["TimeStamp"] = df["TimeStamp"].dt.tz_localize("UTC")
    print(df["TimeStamp"])
    
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

reference_timestamp, laser_on_duration_seconds = find_laser_timeframe(df)
print(reference_timestamp, laser_on_duration_seconds)


#%%
def generate_parameter_data(layer_num, time_offset, x_pos, y_pos, laser_on=True):

    if laser_start_time != 0: 
        laser_on = True
        
    #RPMI values based on literature 
    laser_power = 570 + rng.normal(0, 10.0) #W, mean = 0 and std = 10
    spot_size = 1 + rng.normal(0, 0.1) #mm 
    scan_speed = 660 + rng.normal(0, 10.0) #mm/min
    layer_thickness = 0.65 + rng.normal(0, .2) #mm
    dead_move_speed = 1016 +rng.normal(0, 10.0) #mm/min 
    contour_speed = 660 + rng.normal(0, 10.0) #mm/min 
    stand_off_distance = 6 + rng.normal(0, 0.2)  #mm 
    hatch_width = 0.66 + rng.normal(0, 0.1)  #mm 

    # Melt pool intensity depends on laser state and position
    if laser_on:
        melt_pool_intensity = 0.8 + 0.1 * np.sin(x_pos * 0.1) + rng.normal(0, 0.02)
    else:
        melt_pool_intensity = rng.normal(0.05, 0.01)  # Background noise
    


def generate_machine_data(layer_num, time_offset, x_pos, y_pos, laser_on=True):
