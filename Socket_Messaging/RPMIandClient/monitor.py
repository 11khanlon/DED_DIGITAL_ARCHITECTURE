import csv
import time
import pandas as pd


#%% Laser detection logic, create timestamp
def process_row(row, previous_laser_state, conn):

    try:
        timestamp = pd.to_datetime(row["TimeStamp"], errors="coerce")

        if pd.isna(timestamp):
            return previous_laser_state

        if timestamp.tzinfo is None:
            timestamp = timestamp.tz_localize("UTC")

        laser_state = float(row["Laser On"])

    except Exception:
        return previous_laser_state

    # OFF → ON
    if previous_laser_state == 0 and laser_state != 0:

        msg = f"LASER_ON,{timestamp}"
        print(msg)
        conn.send(msg.encode())

    # ON → OFF
    if previous_laser_state != 0 and laser_state == 0:

        msg = f"LASER_OFF,{timestamp}"
        print(msg)
        conn.send(msg.encode())

    return laser_state

#%% Real-time CSV monitoring
'''
Need to find filepath later 

'''
def tail_csv(filepath, running_flag, conn):

    print("Monitoring CSV:", filepath)

    previous_laser_state = 0

    with open(filepath, "r") as f:

        reader = csv.DictReader(f)

        # Process existing rows
        for row in reader:
            previous_laser_state = process_row(
                row,
                previous_laser_state,
                conn
            )

        # Real-time monitoring loop
        while running_flag["running"]:

            position = f.tell()
            line = f.readline()

            if not line:
                time.sleep(0.2)
                f.seek(position)

            else:
                values = line.strip().split(",")
                row = dict(zip(reader.fieldnames, values))

                previous_laser_state = process_row(
                    row,
                    previous_laser_state,
                    conn
                )