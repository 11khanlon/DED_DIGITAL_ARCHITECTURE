import pandas as pd 
import numpy as np 
import sys 
sys.path.append("C:/Users/Kayleigh/DIGITAL_ARCH_REPO/RPMI_DATA_DEV/ontology_development/ontology_iteration2")
from ingestion.parameter_inputs import toolpath_parameters

'''
defines "allowed vocabulary" of process parameters 

it answers: what is a valid process parameter?, what does it mean, what unit should it have, what system does it belong to? 

how something happened

static ontology

'''

#import process paramters later 
process_control_plan = toolpath_parameters["parameter_id"]

print("Shape of process control plan:")
print(np.shape(process_control_plan))

print("Process control plan:")
print(process_control_plan) 

def build_process_module(process_parameters):

    df = (
        process_parameters
        .drop_duplicates(subset=["parameter_id"])
        .reset_index(drop=True)
    )
    process_df = pd.concat([df, process_control_plan], ignore_index=True)
    return process_df


