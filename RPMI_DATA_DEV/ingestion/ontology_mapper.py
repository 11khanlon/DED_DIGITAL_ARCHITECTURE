import pandas as pd

mapping_df = pd.read_csv(
    "../ontology/mappings/parameter_mappings.csv"
)

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