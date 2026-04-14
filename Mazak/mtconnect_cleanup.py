#%%
import numpy as np 
import pandas as pd 
import time
import sqlite3 
from datetime import datetime
import csv 
import os

#%%
#create dataframe and est. directory 

os.chdir(r"C:\Users\Kayleigh\DIGITAL_ARCH_REPO\Mazak")
df = pd.read_csv("mtconnect_changes_20260320_151239.csv")

#%%
#Rearrange data and make columns and rows

# Pivot the table
pivot_df = df.pivot_table(
    index="Change Timestamp",
    columns="Variable",
    values="New Value",
    aggfunc="first"
).reset_index()

# Optional: enforce column order
columns_order = [
    "Change Timestamp",
    "xpostn", "ypostn", "zpostn",
    "xlod", "ylod", "zlod",
    "fact", "toolnum", "program"
]

pivot_df = pivot_df.reindex(columns=columns_order)
print(pivot_df.shape)

pivot_df.to_csv("test.csv", index=False)


# %%
