#%%
import numpy as np
import pandas as pd
import os

#%%
# --- Load data ---
os.chdir(r"C:\Users\Kayleigh\DIGITAL_ARCH_REPO\RPMI_DATA_DEV")
df = pd.read_csv("dlog_2023-08-09_1106_purge testing.csv", low_memory=False)

original_shape = df.shape
print(f"Original data shape: {original_shape}")

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
    "PF1 Override",
    "PF2 Override",
    "PF3 Override",
    "PF4 Override",
    "PF1 Argon: Warning Enabled",
    "PF1 Argon: Alarm Enabled",
    "PF1 Argon: Baseline Level",
    "PF1 Argon: Warning Tolerance Level",
    "PF1 Argon: Alarm Tolerance Level",
    "PF1 Argon: Valid Value",
    "PF2 Argon: Warning Enabled",
    "PF2 Argon: Alarm Enabled",
    "PF2 Argon: Baseline Level",
    "PF2 Argon: Alarm High Level",
    "PF1 Argon: Alarm High Level",
    "PF1 Argon: Alarm Low Level",
    "PF2 Argon: Alarm Low Level",
    "PF2 Argon: Warning Tolerance Level",
    "PF2 Argon: Alarm Tolerance Level",
    "PF2 Argon: Valid Value",
    "PF3 Argon: Warning Tolerance Level",
    "PF3 Argon: Alarm Enabled",
    "PF3 Argon: Alarm High Level",
    "PF3 Argon: Alarm Low Level",
    "PF3 Argon: Warning Tolerance Level",
    "PF3 Argon: Alarm Tolerance Level",
    "PF3 Argon: Baseline Level",
    "PF3 Argon: Valid Value",
    "PF4 Argon: Warning Enabled",
    "PF4 Argon: Alarm Enabled",
    "PF4 Argon: Baseline Level",
    "PF4 Argon: Valid Value",
    "PF4 Argon: Alarm High Level",
    "PF4 Argon: Alarm Low Level",
    "PF4 Argon: Warning Tolerance Level",
    "PF4 Argon: Alarm Tolerance Level",
    "Center Purge Argon: Warning Enabled",
    "Center Purge Argon: Alarm Enabled",
    "Center Purge Argon: Baseline Level",
    "Center Purge Argon: Valid Value",
    "Center Purge Argon: Alarm High Level",
    "Center Purge Argon: Alarm Low Level",
    "Center Purge Argon: Warning Tolerance Level",
    "Center Purge Argon: Alarm Tolerance Level",
    "Center Purge Pressure: Warning Enabled",
    "Center Purge Pressure: Alarm Enabled",
    "Center Purge Pressure: Baseline Level",
    "Center Purge Pressure: Valid Value",
    "Center Purge Pressure: Alarm High Level",
    "Center Purge Pressure: Alarm Low Level",
    "Center Purge Pressure: Warning Tolerance Level",
    "Center Purge Pressure: Alarm Tolerance Level",
    "H2O Sensor: Warning Enabled",
    "H2O Sensor: Alarm Enabled",
    "O2 Sensor: Warning Enabled",
    "O2 Sensor: Alarm Enabled",
    "O2 Sensor: Alarm High Level",
    "O2 Sensor: Alarm Low Level",
    "H2O Sensor: Alarm High Level",
    "H2O Sensor: Alarm Low Level",
    "Head Temp: Warning Enabled",
    "Head Temp: Alarm Enabled",
    "Head Temp: Alarm High Level",
    "Head Temp: Alarm Low Level",
    "PF1 Bottom Pressure: Baseline Level",
    "PF1 Bottom Pressure : Valid Value",
    "PF1 Bottom Pressure : Warning Enabled",
    "PF1 Bottom Pressure : Alarm Enabled",
    "PF1 Bottom Pressure : Alarm Tolerance Level",
    "PF1 Bottom Pressure : Alarm High Level",
    "PF1 Bottom Pressure : Alarm Low Level",
    "PF1 Bottom Pressure: Off Baseline",
    "PF1 Bottom Pressure: Warning Tolerance Level",
    "Center Purge Pressure: Warning High Level",
    "Center Purge Pressure: Warning Low Level",
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
    "Dryrun Mode",
    "DI Water Temp (Â°C)",
    "Cmd Mode",
    "DeadMove Override",
    "Block Number",
    "Monitoring Enabled",
    "In Warning",
    "In Alarm",
    "Events",
    "Contour Override",
    "Hatch Override"
]

#%%
# --- Filter column names ---
filtered_columns = df.drop(columns=columns_to_drop, errors='ignore').columns.tolist()
final_shape = (df.shape[0], len(filtered_columns))
print(f"Final data shape after dropping columns: {final_shape}")

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

# %%
#--Create ontology table with parameter names and descriptions--

position_data = pd.DataFrame({
    "parameter_name": ["Pos X(inch)", "Pos Y(inch)", "Pos Z(inch)", "Layer #"],
    "description": [
        "X position of the laser head in inches",
        "Y position of the laser head in inches",
        "Z position of the laser head in inches",
        "Current layer number"
    ]
})

velocity_data = pd.DataFrame({
    "parameter_name": ["Velocity X", "Velocity Y", "Velocity Z"],    
    "description": [
        "X velocity of the laser head in inches per second",
        "Y velocity of the laser head in inches per second",
        "Z velocity of the laser head in inches per second"
    ]
})

import pandas as pd

laser_data = pd.DataFrame({
    "parameter_name": [
        "Laser On",
        "Pos Alps(inch)",
        "Alps Spot Size(inch)",
        "Optics Box Pressure Sensor",
        "Laser Setpoint",
        "Laser Power (from laser)",
        "Laser Water Flow (L/min)",
        "Laser Water Temp (Â°C)",
        "Laser On Time (ms)",
        "Feed Fiber FFBD (mV)",
        "Process Fiber FFBD (mV)",
        "Power From Meter",
        "Beam Size From Meter (inch)",
        "Beam Pos X From Meter (inch)",
        "Beam Pos Y From Meter (inch)",
        "Power From Meter (uncompensated)",
        "Beam Flags From Meter"
    ],
    "description": [
        "Laser On/Off status",
        "Laser position in Alps coordinate system",
        "Laser spot size in inches",
        "Pressure sensor in optics box",
        "Laser power set by the user",
        "Laser power measured from the laser source",
        "Laser cooling water flow rate",
        "Laser cooling water temperature",
        "Total laser firing time",
        "Feed fiber back reflection voltage",
        "Process fiber back reflection voltage",
        "Measured laser power from meter",
        "Measured beam size",
        "Measured beam X position",
        "Measured beam Y position",
        "Uncompensated power reading",
        "Beam status flags"
    ]
})


machine_head_data = pd.DataFrame({
    "parameter_name": [
        "Motion Compensation Active",
        "Head Temperature (RTD 1)(Â°F)",
        "Head Temp: Warning High Level",
        "Head Temp: Warning Low Level"
    ]
})


hopper_machine_number = pd.DataFrame({
    "parameter_name": ["PF1", "PF2", "PF3", "PF4"],
    "description": [
        "Machine number for hopper 1",
        "Machine number for hopper 2",
        "Machine number for hopper 3",
        "Machine number for hopper 4"
    ]
})


PF1__data = pd.DataFrame({
    "parameter_name": [
        "PF1 RPM",
        "PF1 RPM Setpoint",
        "PF1 Argon MFlow",
        "PF1 Argon: Warning High Level",
        "PF1 Argon: Warning Low Level",
        "PF1 Argon VFlow",
        "PF1 Argon Temp(Â°F)",
        "PF1 Argon Absolute Pressure",
        "PF1 Powder Low",
        "PF1 Powder Low: Warning Enabled",
        "PF1 Powder Low: Alarm Enabled",
        "PF1 Top Pressure",
        "PF1 Bottom Pressure",
        "PF1 Bottom Pressure : Warning High Level",
        "PF1 Bottom Pressure : Warning Low Level"
    ]
})


center_purge_data = pd.DataFrame({
    "parameter_name": [
        "Center Purge Argon MFlow",
        "Center Purge Argon: Warning High Level",
        "Center Purge Argon: Warning Low Level",
        "Center Purge Argon VFlow",
        "Center Purge Argon Temp(Â°F)",
        "Center Purge Argon Absolute Pressure"
    ]
})


H20_Sensor_data = pd.DataFrame({
    "parameter_name": [
        "H2O Sensor",
        "H2O Sensor: Warning High Level",
        "H2O Sensor: Warning Low Level"
    ]
})


O2_Sensor_data = pd.DataFrame({
    "parameter_name": [
        "O2 Sensor",
        "O2 Sensor: Warning High Level",
        "O2 Sensor: Warning Low Level"
    ]
})


RPMI_machine_data = pd.DataFrame({
    "parameter_name": [
        "Box Pressure",
        "Dust Collector Diff Pressure",
        "Powder Manifold Pressure Sensor",
        "Path Setpoint Velocity(inch/min)",
        "Toolcode Execution Time"
    ]
})


melt_pool_data = pd.DataFrame({
    "parameter_name": [
        "Camera Temp(Â°F)",
        "Melt Pool Area",
        "Melt Pool Area: Valid Value"
    ]
})

