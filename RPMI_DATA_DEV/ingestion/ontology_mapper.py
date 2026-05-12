'''
File only maps telemetry data to ontology parameters
should not ingest SQL
conducts semantic mappings 

'''
#%%
import pandas as pd

mapping_df = pd.read_csv(
    r"C:\Users\Kayleigh\DIGITAL_ARCH_REPO\RPMI_DATA_DEV\ontology\mappings\parameter_mappings.csv"
)

#%%
def map_parameter(column_name):

    c = column_name.lower()

    for _, row in mapping_df.iterrows():

        if row["pattern"] in c:

            return {
                "parameter_id": row["parameter_id"],
                "parameter_name": row["parameter_name"],
                "parameter_type": row["parameter_type"],
                "system_id": row["system_id"],
                "unit": row["unit"],
                "data_type": row["data_type"]
            }

    return None