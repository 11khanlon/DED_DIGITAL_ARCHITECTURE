import os
import numpy as np
import pandas as pd

from ingestion.clean_data import clean_columns
from mapping.parameter_map import convert_to_tic
from modules.TIC import build_tic_observations, build_thermocouple_tic
from modules.PROCESS import build_process_module
#from modules.BUILD import create_build_parameters
#from modules.MATERIAL import MATERIAL_MODULE_EXPORTS, build_material_module

# --------- LOAD RPMI MACHINE DATA ------------
os.chdir(r"C:\Users\Kayleigh\DIGITAL_ARCH_REPO\RPMI_DATA_DEV\data_csv_examples")
df = pd.read_csv("dlog_2023-08-09_1106_purge_testing.csv", low_memory=False)

#-------------- LOAD THERMOCOUPLE DATA --------------
csv_path = r"C:\Users\Kayleigh\DIGITAL_ARCH_REPO\RPMI_DATA_DEV\data_csv_examples\PYRAMID.csv"

#---------------- CLEAN ----------------
parameter_table, cleaned_df = clean_columns(df)


#---------------- PARAMETER MAPPING ----------------
tic_df, process_parameters = convert_to_tic(cleaned_df)



#---------------- TIC ASSEMBLE MODULES ----------------
tic_observations = build_tic_observations(tic_df)  #THIS IS THE MACHINE TIC DATA/TABLE
thermocouple_observations = build_thermocouple_tic(csv_path) #THIS IS THE THERMOCOUPLE TIC DATA/TABLE

print("_______MACHINE TIC OBSERVATIONS_______")
print(tic_observations)

print("_______THERMOCOUPLE TIC OBSERVATIONS_______")
print(thermocouple_observations)


#-------------- PROCESS ASSEMBLE MODULES --------------
process_df = build_process_module(process_parameters) #Table for processes
print("_______PROCESS DATA_______")
print(process_df)



'''
build_df = create_build_parameters(tic_df)

build_params = create_build_parameters(tic_df)

build_material = MATERIAL_MODULE_EXPORTS["build_material_link"]
'''

