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
#Host Server Structure 
HOST = "0.0.0.0"    #insert IP
PORT = 5000         #create port for custom protocol

running = False
print("SCRIPT STARTED")
#%% Find latest CSV produced by RPMI

def get_latest_csv(folder):

    #files = [f for f in os.listdir(folder) if f.endswith(".csv")]
    files = []

    for f in os.listdir(folder):

        if f.endswith(".csv"):
            files.append(f)

    if not files:
        return None

    files.sort(key=lambda x: os.path.getmtime(os.path.join(folder, x)))

    return os.path.join(folder, files[-1])

folder = r"C:\\Users\\Kayleigh\\DIGITAL_ARCH_REPO\\RPMI_DATA_DEV\\random_data"   #INSERT ACTUAL FILE PATH
files2 = get_latest_csv(folder)
print(files2)
print("All CSV files:", files2)
#Note this is a function because we do not know the filepath that the RPMI saves yet

#%% Laser detection logic 
def process_row(row, previous_laser_state):

    try:

        timestamp = pd.to_datetime(row["TimeStamp"], errors="coerce")

        if pd.isna(timestamp):
            return previous_laser_state

        if timestamp.tzinfo is None:
            timestamp = timestamp.tz_localize("UTC")

        laser_state = float(row["Laser On"])

    except Exception:
        return previous_laser_state

    # Laser OFF → ON
    if previous_laser_state == 0 and laser_state != 0:

        print("LASER ON DETECTED")
        print("Start timestamp:", timestamp)

    # Laser ON → OFF
    if previous_laser_state != 0 and laser_state == 0:

        print("LASER OFF DETECTED")
        print("Stop timestamp:", timestamp)

    return laser_state

#%% Real Time Engine -- This function writes the CSV file continuosly
#how does this work with the past funciton?
def read_rpmi_csv(filepath):
    with open(filepath, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            print(row)



#%% Real-time CSV monitoring
def tail_csv(filepath):

    global running

    print("Monitoring CSV:", filepath)

    previous_laser_state = 0

    with open(filepath, "r") as f:

        reader = csv.DictReader(f)

        # Process existing rows first
        for row in reader:

            previous_laser_state = process_row(row, previous_laser_state)

        # Monitor new rows written by RPMI
        while running:

            position = f.tell()
            line = f.readline()

            if not line:
                time.sleep(0.2)
                f.seek(position)

            else:

                values = line.strip().split(",")

                row = dict(zip(reader.fieldnames, values))

                previous_laser_state = process_row(row, previous_laser_state)


#%% Socket Server
def start_server():

    global running

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.bind((HOST, PORT))

    server.listen(1)

    print("Server waiting for connection...")

    conn, addr = server.accept()

    print("Connected by", addr)

    while True:

        data = conn.recv(1024).decode().strip()

        if not data:
            break

        print("Received:", data)

        if data == "START":

            print("Starting RPMI monitoring")

            latest_file = get_latest_csv(RPMI_FOLDER)

            if latest_file is None:

                print("No CSV files found")
                continue

            running = True

            tail_csv(latest_file)

        elif data == "STOP":

            print("Stopping monitoring")

            running = False

        elif data == "PING":

            conn.send("ALIVE".encode())

    conn.close()


#%% Run server
start_server()


#%%

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