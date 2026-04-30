import pandas as pd

def get_laser_start_event(df):

    df = df.copy()

    df["TimeStamp"] = pd.to_datetime(df["TimeStamp"], errors="coerce")
    df = df.dropna(subset=["TimeStamp"]).reset_index(drop=True)

    # timezone safe
    if df["TimeStamp"].dt.tz is None:
        df["TimeStamp"] = df["TimeStamp"].dt.tz_localize("UTC")
    else:
        df["TimeStamp"] = df["TimeStamp"].dt.tz_convert("UTC")

    laser_idx = df.index[df["Laser On"] != 0]

    if len(laser_idx) == 0:
        return df, None

    start_idx = laser_idx[0]

    return df, df.loc[start_idx, "TimeStamp"]