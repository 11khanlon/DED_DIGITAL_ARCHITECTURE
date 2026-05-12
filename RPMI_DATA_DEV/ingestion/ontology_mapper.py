'''
File only maps telemetry data to ontology parameters
should not ingest SQL
conducts semantic mappings 

'''
#%%
import pandas as pd
import re

mapping_df = pd.read_csv(
    r"C:\Users\Kayleigh\DIGITAL_ARCH_REPO\RPMI_DATA_DEV\ontology\mappings\parameter_mappings.csv"
)


#%%
# NORMALIZATION
def normalize(col):
    col = col.lower().strip()
    col = re.sub(r"[^a-z0-9 ]", " ", col)
    col = re.sub(r"\s+", " ", col)
    return col

#%%
# =========================================================
# PREPROCESS ONTOLOGY TABLE (IMPORTANT IMPROVEMENT)
# =========================================================
mapping_df["pattern_norm"] = mapping_df["pattern"].apply(normalize)


# =========================================================
# CORE MAPPING FUNCTION (ONTOLOGY DRIVEN)
# =========================================================
def map_parameter(column_name: str):

    col_norm = normalize(column_name)

    best_match = None
    best_score = 0

    # -----------------------------------------------------
    # MATCHING STRATEGY: longest pattern wins (IMPORTANT)
    # -----------------------------------------------------
    for _, row in mapping_df.iterrows():

        pattern = row["pattern_norm"]

        # exact or substring match
        if pattern in col_norm:

            score = len(pattern)

            # keep MOST SPECIFIC match
            if score > best_score:
                best_score = score

                best_match = {
                    "parameter_id": row["parameter_id"],
                    "parameter_name": row["parameter_name"],
                    "parameter_type": row["parameter_type"],
                    "system_id": row["system_id"],
                    "unit": row["unit"],
                    "data_type": row["data_type"]
                }

    return best_match