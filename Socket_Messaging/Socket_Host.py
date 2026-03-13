#%%
import numpy as np 
import pandas as pd 
from datetime import datetime
import csv 
import os

#import requests
import time
#import xmltodict
import json
import socket 
import threading 
import sqlite3 


#%%
'''
START_RUN = begin logging
STOP_RUN = end logging
PING = check connection 
RUN_COMPLETE  = host finished logging
'''
#%%
#Host Server Structure 
HOST = "0.0.0.0"
PORT = 5000


def read_rpmi_csv(filepath):
    with open(filepath, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            print(row)

def start_server():

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(1)

    print("Server waiting for connection...")

    conn, addr = server.accept()
    print("Connected by", addr)

    while True:

        data = conn.recv(1024).decode()

        if not data:
            break

        if data == "START":
            print("Starting logging")
            read_rpmi_csv("run_file.csv")

        elif data == "STOP":
            print("Stopping run")

        elif data == "PING":
            conn.send("ALIVE".encode())

    conn.close()

start_server()


#%%
# --- Load data and get column values ---
os.chdir(r"C:\Users\Kayleigh\DIGITAL_ARCH_REPO\RPMI_DATA_DEV\output_files")
df = pd.read_csv("dlog_2023-08-09_1106_purge testing.csv", low_memory=False)

#%%
# --- Get column names and Laser on timestamp ---
columns = df.columns 
column_names1 = df.columns.tolist()
print(column_names1)
column_names = pd.Series(df.columns)
column_names.to_csv("RPMI_column_names.csv", index=False, header=False)

#%%

'''need to add timestamp, set to UTC. timestamp once the folder is available. 
If available and the laser is on, create a string saying Good to start reading, then create a timestamp. 
When the laser is turned off - check laser on time - then timestamp the folder that process has ended 
Maybe, we do not need to cleanup the rows for later?
Compile data on host computer, then send to client to avoid lag. 
Maybe look into python watchdog import
'''

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