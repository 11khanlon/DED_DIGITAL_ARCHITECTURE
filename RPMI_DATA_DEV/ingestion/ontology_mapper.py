import pandas as pd
import sys 
import os 
import re


# --------- LOAD RPMI MACHINE DATA ------------
os.chdir(r"C:\Users\Kayleigh\DIGITAL_ARCH_REPO\RPMI_DATA_DEV\data_csv_examples")
df = pd.read_csv("dlog_2023-08-09_1106_purge_testing.csv", low_memory=False)


sys.path.append(
    r"C:\Users\Kayleigh\DIGITAL_ARCH_REPO\RPMI_DATA_DEV\ontology\mappings")
mapping_df = pd.read_csv("parameter_mappings.csv")




def map_parameter(column_name):

    c = column_name.lower()

    for _, row in mapping_df.iterrows():

        if row["pattern"] in c:

            return {
                "parameter_id": row["parameter_id"],
                "parameter_name": row["parameter_name"],
                "system_id": row["system_id"],
                "unit": row["unit"],
                "data_type": row["data_type"]
            }

    return None


mapping = map_parameter(col)

if mapping is None:
    continue

parameter_id = mapping["parameter_id"]

system_id = mapping["system_id"]

unit = mapping["unit"]