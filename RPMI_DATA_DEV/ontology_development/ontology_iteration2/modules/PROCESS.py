import pandas as pd 
import numpy as np 

'''
defines "allowed vocabulary" of process parameters 

it answers: what is a valid process parameter?, what does it mean, what unit should it have, what system does it belong to? 

how something happened

static ontology

'''

def build_process_module(tic_df, process_parameters):

    # SAFE join (left join only)
    process_df = tic_df.merge(
        process_parameters,
        on="parameter_id",
        how="left",
        validate="m:1"   # IMPORTANT safety guard
    )

    return process_df


#import process paramters later 
def build_process_control_plan():
    return pd.DataFrame({
        "control_plan_id": [],
        "parameter_id": [],
        "target_value": [],
        "unit": [],
        "process_version": [],
    })


'''
Laser Spot Size (In): 0.070 
Laser Power (W): 1070 
Head Type: RPMI 45 Degree Powder Nozzle 
Type: 002-0021-004 - STEEP WALL POWDER NOZZLE Nozzle Change Interval (Hrs): 18 
Standoff - Working Height from bottom of powder nozzles (In): 0.250” Powder Feed Rate (Grams per minute – GPM): 16.00 (IN 718) and 15.20 (316 SS) 
Layer Thickness (In): 0.015 
Hatch Width (In): 0.045 
Hatch Angles (Degrees): 0, 45, 90, 135, 180, 225, 270, 315 Model Offset (If needed) (In): 0.035 
After Layer Wait (milliseconds): 10000 yea but these are input paraemters to the toolpath generator
maybe put this is a csv file?
'''