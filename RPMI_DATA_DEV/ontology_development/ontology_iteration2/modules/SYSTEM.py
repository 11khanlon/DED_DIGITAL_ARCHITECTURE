#%%
import pandas as pd
import numpy as np

#%%

'''
all hardware - These are physical things 
This includes all gas delivery systems (PF1-PF4, CP1)
Optics (OPT1, subsystems)
Machine head (MH1) 
Sensors (interal and external)

static ontology

'''

systems = pd.DataFrame({
    "system_id": [
        "RPMI_01",
        "PF1", "PF2", "PF3", "PF4",
        "CP1",
        "LASER_01",
        "MH1",
        "CAM_01",
        "TC",
        "O2_SENSOR",
        "H2O_SENSOR"
    ],
    "system_type": [
        "machine",
        "hopper", "hopper", "hopper", "hopper",
        "purge_line",
        "optics/laser",
        "machine_head",
        "camera",
        "thermocouple",
        "gas_sensor",
        "gas_sensor"
    ],
    "parent_system": [
        None,
        "RPMI_01", "RPMI_01", "RPMI_01", "RPMI_01",
        "RPMI_01",
        "RPMI_01",
        "RPMI_01",
        "RPMI_01",       
        "MH1",         # thermocouples tied to build plate/head
        "RPMI_01",
        "RPMI_01"
    ]
})

print(systems)
# %%
