#%%
import numpy as np
import pandas as pd
import os
import sys
sys.path.append(
    r"C:\\Users\\Kayleigh\\DIGITAL_ARCH_REPO\\RPMI_DATA_DEV"
)
from ingestion.columns_to_drop import columns_to_drop



#%%



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


    print("\n--- END CLEANING PIPELINE ---\n")

    return parameter_table, filtered



csv_path = (
    r"C:\Users\Kayleigh\DIGITAL_ARCH_REPO"
    r"\RPMI_DATA_DEV\data_csv_examples"
    r"\dlog_2026-04-02_1209_TestPrintInconel718Boeing.csv"
)

parameter_table, cleaned_df = clean_columns(pd.read_csv(csv_path))