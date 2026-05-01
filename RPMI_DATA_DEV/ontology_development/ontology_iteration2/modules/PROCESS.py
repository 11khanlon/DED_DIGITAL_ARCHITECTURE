import pandas as pd 
import numpy as np 

'''
defines "allowed vocabulary" of process parameters 

it answers: what is a valid process parameter?, what does it mean, what unit should it have, what system does it belong to? 


'''

def build_process_module(tic_df,process_parameters):
    # 1. extract observed parameters from data
    observed = (
        tic_df[["parameter_id", "unit"]]
        .dropna()
        .drop_duplicates()
    )

    # 2. join semantic definitions
    process_df = observed.merge(
        process_parameters,
        on="parameter_id",
        how="left"
    )

    # 3. reorder for clarity
    process_df = process_df[[
        "parameter_id",
        "description",
        "unit"
    ]]

    return process_df

