#%%
import numpy as np
import pandas as pd
import os


#%%
# --- Columns to drop ---

#move this to data section later, but for now it's here for easy access and editing
columns_to_drop = [
    "Assum Pos Z(inch)",
    "Pos Tilt",
    "Pos Rotate",
    "Pho X(inch)",
    "Pho Y(inch)",
    "Pho Z(inch)",
    "Pho Tilt",
    "Pho Rotate",
    "Velocity Tilt", #Assume rotate and tilt with their respective velocities are 0
    "Velocity Rotate", 
    "PF1 Override",  #drop redundant warnings
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

print(f"Shape of columns_to_drop: {len(columns_to_drop)}")

#%%
'''RPMI_machine_data = pd.DataFrame({
    "parameter_name": [
        "Box Pressure",
        "Dust Collector Diff Pressure",
        "Powder Manifold Pressure Sensor",
        "Path Setpoint Velocity(inch/min)",
        "Toolcode Execution Time"
    ]
})
Path setpoint velocity is the set federate / print speed.
Dust collector is the filtration pressure differential. 
Powder manifold is I think some pressure difference between top and bottom hopper. 
Toolcode Execution time is either the time spent running or th etime estimated I believe

 variables that are helpful for RPMI, but I won't know until I print'''


def clean_columns(df):

    print("\n--- START CLEANING PIPELINE ---")

    original_shape = df.shape
    print(f"Original shape: {original_shape}")

    # Clean column names
    df.columns = (
        df.columns
        .str.strip()
        .str.replace('\ufeff', '', regex=False)
    )
   
    metadata = None
    if df.shape[0] >= 5:
        metadata = {
            "file_name": str(df.iloc[0, 0]),
            "start_time": str(df.iloc[1, 0]),
            "title": str(df.iloc[2, 0]),
            "units": str(df.iloc[3, 0]),
            "notes": str(df.iloc[4, 0]),
        }

        print("\n--- METADATA ---")
        for k, v in metadata.items():
            print(f"{k}: {v}")

    df = df.iloc[5:].reset_index(drop=True)

    # Ensure required columns exist
    if "TimeStamp" not in df.columns:
        raise ValueError(f"Missing TimeStamp. Columns: {df.columns.tolist()}")
    df["TimeStamp"] = pd.to_datetime(
    df["TimeStamp"],
    format="%Y/%m/%d %I:%M:%S.%f %p",
    errors="coerce"
   )

    df = df.dropna(subset=["TimeStamp"]).reset_index(drop=True)
    df["TimeStamp"] = df["TimeStamp"].dt.tz_localize("UTC")

    print(f"\nShape after timestamp cleaning: {df.shape}")


    # --- Drop predefined columns ---
    print(f"\nAttempting to drop {len(columns_to_drop)} predefined columns...")

    existing_drop_cols = [c for c in columns_to_drop if c in df.columns]
    missing_drop_cols = [c for c in columns_to_drop if c not in df.columns]

    print(f"Columns FOUND and dropped: {len(existing_drop_cols)}")
    print(existing_drop_cols[:10], "...")

    print(f"Columns NOT found (already gone or never existed): {len(missing_drop_cols)}")
    print("\n MISSING DROP COLUMN\n")
    for col in missing_drop_cols:
        print(col)


    filtered = df.drop(columns=columns_to_drop, errors="ignore")

    print(f"\nShape after predefined drop: {filtered.shape}")

    # Save outputs
    filtered.to_csv("cleaned_original.csv", index=False)

    pd.DataFrame(filtered.columns, columns=["Variable_Names"]).to_csv(
        "cleaned_variable_names.csv", index=False
    )

    cleaned_shape = filtered.shape

    summary = (
        f"\n--- SUMMARY ---\n"
        f"Original: {original_shape}\n"
        f"Final:    {cleaned_shape}\n"
        f"Cols removed: {original_shape[1] - cleaned_shape[1]}\n"
        f"Rows removed: {original_shape[0] - cleaned_shape[0]}\n"
    )

    print(summary)

    with open("cleanup_summary.txt", "w") as f:
        f.write(summary)

    # Parameter table
    parameter_table = pd.DataFrame({
        "parameter_id": range(1, len(filtered.columns) + 1),
        "parameter_name": filtered.columns
    })

    print("\nFinal columns preview:")
    print(filtered.columns[:10].tolist(), "...")

    print("\n--- END CLEANING PIPELINE ---\n")

    return parameter_table, filtered

