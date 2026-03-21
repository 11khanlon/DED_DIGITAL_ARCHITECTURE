#%%
import numpy as np 
import pandas as pd 
from datetime import datetime
import csv 
import os

import time
import json
import socket 
import threading 
import sqlite3 


#%%
#Host Server Structure 
HOST = "0.0.0.0"    #insert IP
PORT = 5000         #create port for custom protocol

running = False

#%% Find latest CSV produced by RPMI
'''
#Note this is a function because we do not know the filepath that the RPMI saves yet
'''

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

folder = r"C:\\Users\\Kayleigh\\DIGITAL_ARCH_REPO\\RPMI_DATA_DEV\\data_csv_examples"   #INSERT ACTUAL FILE PATH
RPMI_FOLDER = get_latest_csv(folder)

#%% Laser detection logic, create timestamp
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


#%% Real-time CSV monitoring
'''
Need to find filepath later 

'''
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