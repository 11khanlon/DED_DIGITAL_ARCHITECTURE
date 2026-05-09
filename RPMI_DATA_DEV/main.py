import os
import numpy as np
import pandas as pd

from RPMI_DATA_DEV.ingestion.clean_data import clean_columns
from RPMI_DATA_DEV.ontology.parameter_map import convert_to_tic
from RPMI_DATA_DEV.database.modules.TIC import build_tic_observations, build_thermocouple_tic
from RPMI_DATA_DEV.database.modules.PROCESS import build_process_module
from RPMI_DATA_DEV.database.modules.BUILD import create_build_parameters, create_build_module
#from modules.MATERIAL import MATERIAL_MODULE_EXPORTS, build_material_module

# --------- LOAD RPMI MACHINE DATA ------------
os.chdir(r"C:\Users\Kayleigh\DIGITAL_ARCH_REPO\RPMI_DATA_DEV\data_csv_examples")
df = pd.read_csv("dlog_2023-08-09_1106_purge_testing.csv", low_memory=False)

#-------------- LOAD THERMOCOUPLE DATA --------------
csv_path = r"C:\Users\Kayleigh\DIGITAL_ARCH_REPO\RPMI_DATA_DEV\data_csv_examples\PYRAMID.csv"

#load process parameters later 


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

print("_______PROCESS MODULE_______")
print(process_df)

'''#------ BUILD ASSEMBLE MODULE ------
build_df = create_build_module(tic_df)
create_build_parameters= create_build_parameters(tic_df, thermocouple_observations)

print("_______BUILD MODULE_______")
print(build_df)'''
