import numpy as np
import pandas as pd
import os

#%%
# --- Load data ---
os.chdir(r"C:\Users\Kayleigh\DIGITAL_ARCH_REPO\RPMI_DATA_DEV")
df = pd.read_csv("dlog_2023-08-09_1106_purge testing.csv", low_memory=False)

#%%
# --- Columns to drop ---
#Assume rotate and tilt with their respective velocities are 0, drop redundant warnings
columns_to_drop = [
    "Assum Pos Z(inch)",
    "Pos Tilt",
    "Pos Rotate",
    "Pho X(inch)",
    "Pho Y(inch)",
    "Pho Z(inch)",
    "Pho Tilt",
    "Pho Rotate",
    "Velocity Tilt",
    "Velocity Rotate",
    "PF1 Argon: Warning Enabled",
    "PF1 Argon: Alarm Enabled",
    "PF2 Argon: Alarm Enabled",
    "PF2 Argon: Baseline Level",
    "PF2 Argon: Valid Value",
    "PF3 Argon: Alarm Enabled",
    "PF3 Argon: Baseline Level",
    "PF3 Argon: Valid Value",
    "PF4 Argon: Alarm Enabled",
    "PF4 Argon: Baseline Level",
    "PF4 Argon: Valid Value",
    "Center Purge Argon: Warning Enabled",
    "Center Purge Argon: Alarm Enabled",
    "Center Purge Argon: Baseline Level",
    "Center Purge Argon: Valid Value",
    "Center Purge Pressure: Warning Enabled",
    "Center Purge Pressure: Alarm Enabled",
    "Center Purge Pressure: Baseline Level",
    "Center Purge Pressure: Valid Value",
    "H2O Sensor: Warning Enabled",
    "H2O Sensor: Alarm Enabled",
    "O2 Sensor: Warning Enabled",
    "O2 Sensor: Alarm Enabled",
    "Head Temp: Warning Enabled",
    "Head Temp: Alarm Enabled",
    "PF1 Bottom Pressure: Baseline Level",
    "PF1 Bottom Pressure : Valid Value",
    "PF1 Bottom Pressure : Warning Enabled",
    "PF1 Bottom Pressure : Alarm Enabled",
    "PF1 Bottom Pressure : Alarm Tolerance Level",
    "PF1 Bottom Pressure : Alarm High Level",
    "PF1 Bottom Pressure : Alarm Low Level",
    "PF1 Bottom Pressure: Off Baseline",
    "PF2 Bottom Pressure: Baseline Level",
    "PF2 Bottom Pressure : Valid Value",
    "PF2 Bottom Pressure : Warning Enabled",
    "PF2 Bottom Pressure: Warning Tolerance Level",
    "PF2 Bottom Pressure : Warning High Level",
    "PF2 Bottom Pressure : Warning Low Level",
    "PF2 Bottom Pressure : Alarm Enabled",
    "PF2 Bottom Pressure : Alarm Tolerance Level",
    "PF2 Bottom Pressure : Alarm High Level",
    "PF2 Bottom Pressure : Alarm Low Level",
    "PF2 Bottom Pressure: Off Baseline",
    "Powder Manifold Pressure: Baseline Level",
    "Powder Manifold Pressure : Valid Value",
    "Powder Manifold Pressure : Warning Enabled",
    "Powder Manifold Pressure: Warning Tolerance Level",
    "Powder Manifold Pressure : Warning High Level",
    "Powder Manifold Pressure : Warning Low Level",
    "Powder Manifold Pressure : Alarm Enabled",
    "Powder Manifold Pressure: Alarm Tolerance Level",
    "Powder Manifold Pressure : Alarm High Level",
    "Powder Manifold Pressure : Alarm Low Level",
    "PF3 Bottom Pressure: Baseline Level",
    "PF3 Bottom Pressure : Valid Value",
    "PF3 Bottom Pressure : Warning Enabled",
    "PF3 Bottom Pressure: Warning Tolerance Level",
    "PF3 Bottom Pressure : Warning High Level",
    "PF3 Bottom Pressure : Warning Low Level",
    "PF3 Bottom Pressure : Alarm Enabled",
    "PF3 Bottom Pressure : Alarm Tolerance Level",
    "PF3 Bottom Pressure : Alarm High Level",
    "PF3 Bottom Pressure : Alarm Low Level",
    "PF3 Bottom Pressure: Off Baseline",
    "PF4 Bottom Pressure: Baseline Level",
    "PF4 Bottom Pressure : Valid Value",
    "PF4 Bottom Pressure : Warning Enabled",
    "PF4 Bottom Pressure: Warning Tolerance Level",
    "PF4 Bottom Pressure : Warning High Level",
    "PF4 Bottom Pressure : Warning Low Level",
    "PF4 Bottom Pressure : Alarm Enabled",
    "PF4 Bottom Pressure : Alarm Tolerance Level",
    "PF4 Bottom Pressure : Alarm High Level",
    "PF4 Bottom Pressure : Alarm Low Level",
    "PF4 Bottom Pressure: Off Baseline",
    "Optics Box Pressure: Baseline Level",
    "Optics Box Pressure: Valid Value",
    "Optics Box Pressure: Warning Enabled",
    "Optics Box Pressure: Warning Tolerance Level",
    "Optics Box Pressure: Warning High Level",
    "Optics Box Pressure: Warning Low Level",
    "Optics Box Pressure: Alarm Enabled",
    "Optics Box Pressure: Alarm Tolerance Level",
    "Optics Box Pressure: Alarm High Level",
    "Optics Box Pressure: Alarm Low Level",
    "Power From Meter: Warning Enabled",
    "Power From Meter: Alarm Enabled",
    "Power From Meter: Baseline Level",
    "Melt Pool Area: Warning Enabled",
    "Melt Pool Area: Warning High Level",
    "Melt Pool Area: Warning Low Level",
    "Melt Pool Area: Alarm Enabled",
    "Melt Pool Area: Alarm High Level",
    "Melt Pool Area: Alarm Low Level",
    "Melt Pool Area: Debounce Time",
    "Melt Pool Area: Baseline Level",
    "Melt Pool Area: Warning Tolerance Level",
    "Melt Pool Area: Alarm Tolerance Level",
    "Error During Execution",
    "Cmd Mode ",
    "DeadMove Override",
    "Block Number",
    "Monitoring Enabled",
    "In Warning",
    "In Alarm",
    "Events"
]

#%%
# --- Filter column names ---
filtered_columns = df.drop(columns=columns_to_drop, errors='ignore').columns.tolist()

#%%
# --- Create parameter table ---
parameter_table = pd.DataFrame({
    "parameter_id": range(1, len(filtered_columns) + 1),
    "parameter_name": filtered_columns
})

#%%
# --- Save to CSV ---
parameter_table.to_csv(
    "RPMI_parameter_table.csv",
    index=False
)

print("Parameter table created successfully.")
