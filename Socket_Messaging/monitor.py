import csv
import time
import pandas as pd


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
