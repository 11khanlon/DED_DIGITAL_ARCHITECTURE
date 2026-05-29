#%%
import numpy as np
import pandas as pd
import os
import sys
import re

sys.path.append(
    r"C:\\Users\\Kayleigh\\DIGITAL_ARCH_REPO\\RPMI_DATA_DEV"
)

from ingestion.columns_to_drop import columns_to_drop


#%%

def clean_columns(df):

    print("\n--- START CLEANING PIPELINE ---")

    original_shape = df.shape
    print(f"Original shape: {original_shape}")

    # =====================================================
    # CLEAN COLUMN NAMES
    # =====================================================

    df.columns = (
        df.columns
        .str.strip()
        .str.replace('\ufeff', '', regex=False)
    )

    # =====================================================
    # SAVE METADATA
    # =====================================================

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

    # remove metadata rows
    df = df.iloc[5:].reset_index(drop=True)

    # =====================================================
    # REQUIRED COLUMNS
    # =====================================================

    if "TimeStamp" not in df.columns:

        raise ValueError(
            f"Missing TimeStamp column.\n"
            f"Columns: {df.columns.tolist()}"
        )

    # =====================================================
    # CLEAN TIMESTAMP
    # =====================================================

    # keep original string timestamp
    df["TimeStamp_Original"] = df["TimeStamp"]

    # parse timestamp
    df["TimeStamp"] = pd.to_datetime(
        df["TimeStamp"],
        format="%M:%S.%f",
        errors="coerce"
    )

    # remove invalid timestamps
    df = df.dropna(
        subset=["TimeStamp"]
    ).reset_index(drop=True)

    # localize timezone
    df["TimeStamp"] = (
        df["TimeStamp"]
        .dt.tz_localize("UTC")
    )

    print(
        f"\nShape after timestamp cleaning: "
        f"{df.shape}"
    )

    # =====================================================
    # FIND TOOL EXECUTION COLUMN
    # =====================================================

    tool_col = None

    possible_tool_cols = [
        "Toolcode Execution Time",
        "Tool code execution time",
        "ToolCodeExecutionTime",
        "Tool Code Execution Time"
    ]

    for col in possible_tool_cols:

        if col in df.columns:

            tool_col = col
            break

    # =====================================================
    # EVENTS COLUMN
    # =====================================================

    events_col = None

    if "Events" in df.columns:
        events_col = "Events"

    # =====================================================
    # MOVE TOOL EXECUTION COLUMN
    # NEXT TO TIMESTAMP
    # =====================================================

    if tool_col is not None:

        cols = list(df.columns)

        cols.remove(tool_col)

        timestamp_index = cols.index("TimeStamp")

        cols.insert(
            timestamp_index + 1,
            tool_col
        )

        df = df[cols]

        print(
            f"\nMoved '{tool_col}' "
            f"next to TimeStamp"
        )

    # =====================================================
    # IDENTIFY EVENT ROWS
    # =====================================================

    event_rows = pd.DataFrame()

    if events_col is not None:

        event_mask = (
            df[events_col]
            .notna()
            &
            (
                df[events_col]
                .astype(str)
                .str.strip()
                != ""
            )
        )

        event_rows = df[event_mask].copy()

        print(
            f"\nEvent rows found: "
            f"{len(event_rows)}"
        )

    # =====================================================
    # DETECT BUILD START EVENT
    # =====================================================

    telemetry_df = df.copy()

    build_event_info = None
    build_file = None
    build_start_index = None

    pre_build_df = pd.DataFrame()
    build_df = pd.DataFrame()

    if events_col is not None:

        execution_mask = (
            telemetry_df[events_col]
            .astype(str)
            .str.contains(
                "Execution Started",
                case=False,
                na=False
            )
        )

        # -------------------------------------------------
        # BUILD EVENT FOUND
        # -------------------------------------------------

        if execution_mask.any():

            build_start_index = (
                execution_mask.idxmax()
            )

            build_event_row = telemetry_df.loc[
                build_start_index
            ]

            build_event_info = (
                build_event_row[events_col]
            )

            print(
                "\n--- BUILD START DETECTED ---"
            )

            print(build_event_info)

            # ---------------------------------------------
            # EXTRACT MPF FILE
            # ---------------------------------------------

            match = re.search(
                r'Execution Started:\s*(.*?\.mpf)',
                str(build_event_info)
            )

            if match:

                build_file = match.group(1)

                print("\nBuild file detected:")
                print(build_file)

            # ---------------------------------------------
            # SPLIT DATA
            # ---------------------------------------------

            pre_build_df = telemetry_df.loc[
                :build_start_index - 1
            ].reset_index(drop=True)

            build_df = telemetry_df.loc[
                build_start_index + 1:
            ].reset_index(drop=True)

            print(
                f"\nPre-build rows: "
                f"{len(pre_build_df)}"
            )

            print(
                f"Build telemetry rows: "
                f"{len(build_df)}"
            )

        # -------------------------------------------------
        # NO BUILD EVENT
        # -------------------------------------------------

        else:

            print(
                "\nNo execution event found."
            )

            print(
                "Likely purge/no-build dataset."
            )

            pre_build_df = telemetry_df.copy()

            build_df = pd.DataFrame()

    else:

        print(
            "\nNo Events column found."
        )

        pre_build_df = telemetry_df.copy()

    # =====================================================
    # REMOVE EVENTS FROM DROP LIST
    # =====================================================

    safe_drop_cols = [
        c for c in columns_to_drop
        if c != "Events"
    ]

    # =====================================================
    # DROP COLUMNS
    # =====================================================

    print(
        f"\nAttempting to drop "
        f"{len(safe_drop_cols)} columns..."
    )

    existing_drop_cols = [
        c for c in safe_drop_cols
        if c in build_df.columns
    ]

    missing_drop_cols = [
        c for c in safe_drop_cols
        if c not in build_df.columns
    ]

    print(
        f"Columns FOUND and dropped: "
        f"{len(existing_drop_cols)}"
    )

    print(existing_drop_cols[:10], "...")

    print(
        f"\nColumns NOT found: "
        f"{len(missing_drop_cols)}"
    )

    filtered = build_df.drop(
        columns=safe_drop_cols,
        errors="ignore"
    )

    # =====================================================
    # SAVE OUTPUTS
    # =====================================================

    filtered.to_csv(
        "cleaned_original.csv",
        index=False
    )

    pd.DataFrame(
        filtered.columns,
        columns=["Variable_Names"]
    ).to_csv(
        "cleaned_variable_names.csv",
        index=False
    )

    # -----------------------------------------------------
    # SAVE EVENT ROWS
    # -----------------------------------------------------

    if len(event_rows) > 0:

        event_rows.to_csv(
            "event_rows.csv",
            index=False
        )

    # -----------------------------------------------------
    # SAVE PRE-BUILD TELEMETRY
    # -----------------------------------------------------

    if len(pre_build_df) > 0:

        pre_build_df.to_csv(
            "pre_build_telemetry.csv",
            index=False
        )

    # -----------------------------------------------------
    # SAVE BUILD TELEMETRY
    # -----------------------------------------------------

    if len(build_df) > 0:

        build_df.to_csv(
            "build_telemetry.csv",
            index=False
        )

    # =====================================================
    # SUMMARY
    # =====================================================

    cleaned_shape = filtered.shape

    summary = (
        f"\n--- SUMMARY ---\n"
        f"Original Shape: {original_shape}\n"
        f"Final Shape:    {cleaned_shape}\n"
        f"Columns Removed: "
        f"{original_shape[1] - cleaned_shape[1]}\n"
        f"Rows Removed: "
        f"{original_shape[0] - cleaned_shape[0]}\n"
    )

    print(summary)

    with open(
        "cleanup_summary.txt",
        "w"
    ) as f:

        f.write(summary)

    # =====================================================
    # PARAMETER TABLE
    # =====================================================

    parameter_table = pd.DataFrame({

        "parameter_id": range(
            1,
            len(filtered.columns) + 1
        ),

        "parameter_name": filtered.columns
    })

    print("\n--- END CLEANING PIPELINE ---\n")

    return (
        parameter_table,
        filtered,
        metadata,
        build_file,
        pre_build_df,
        build_df,
        event_rows
    )


#%%

csv_path = (
    r"C:\\Users\\Kayleigh\\DIGITAL_ARCH_REPO"
    r"\\RPMI_DATA_DEV\\data_csv_examples"
    r"\\dlog_2026-04-02_1209_TestPrintInconel718Boeing.csv"
)

#Examples:r"\dlog_2023-08-09_1106_purge_testing.csv" r"\dlog_2026-04-02_1209_TestPrintInconel718Boeing.csv"


(
    parameter_table,
    cleaned_df,
    metadata,
    build_file,
    pre_build_df,
    build_df,
    event_rows

) = clean_columns(
    pd.read_csv(csv_path)
)