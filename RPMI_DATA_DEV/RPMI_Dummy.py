import numpy as np 
import pandas as pd 
import time
from datetime import datetime
import csv 
import os 

#%%

"create random data from parameters from the rpmi. Also generate random material data"
" Make them realistic with parameters that I have found from literature "

rng = np.random.default_rng(seed=42) 

# --- Load data and get column values ---
os.chdir(r"C:\Users\Kayleigh\DIGITAL_ARCH_REPO\RPMI_DATA_DEV")
df = pd.read_csv("dlog_2023-08-09_1106_purge testing.csv", low_memory=False)
columns = df.columns 
column_names = df.columns.tolist()
laser_on = df["Laser On"].iloc[0]  # Get the first value in the "Laser On" column
row_numbers = float(df.rows)
print(row_numbers)

'''laser_on_time = df - df["Laser On"].iloc[0]



# --- Track original shape ---
original_shape = df.shape
laser_time = "LaserOn from excel "

def generate_parameter_data(layer_num, time_offset, x_pos, y_pos, laser_on=True):

if laser_time != 0: 
    laser_on = True

    

laser_power = 570 + rng.normal(0, 10.0) #W 
spot_size = 1 #mm 
scan_speed = 660 + rng.normal(0, 10.0) #mm/min
layer_thickness = 0.65 #mm
dead_move_speed = 1016 #mm/min 
contour_speed = 660 #mm/min 
stand_off_distance = 6 #mm 
hatch_width = 0.66   #mm 

# Melt pool intensity depends on laser state and position
    if laser_on:
        melt_pool_intensity = 0.8 + 0.1 * np.sin(x_pos * 0.1) + rng.normal(0, 0.02)
    else:
        melt_pool_intensity = rng.normal(0.05, 0.01)  # Background noise


def generate_machine_data(layer_num, time_offset, x_pos, y_pos, laser_on=True):'''
