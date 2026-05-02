import numpy as np 
import pandas as pd 

'''
this is print_metadata
printparameters, printwarnings, printevents, printstatus
layer count, speed

execution context links everything together 
''' 

builds = pd.DataFrame({
    "build_id": ["PRINT_20260219_01"],
    "machine_id": ["RPMI_01"],
    "material_id": ["MAT_001"],

    "operator": ["Kayleigh Hanlon"],
    "start_time": ["2026-02-19T12:00:00"],
    "end_time": ["2026-02-19T15:30:00"],
    "status": ["Completed"]
})

build_configuration = pd.DataFrame({
    "build_id": ["PRINT_20260219_01"] * 6,
    "parameter_id": [
        "LAYER_HEIGHT",
        "PRINT_SPEED",
        "LASER_POWER_SETPOINT",
        "HATCH_SPACING",
        "POWDER_FEED_RATE",
        "SCAN_STRATEGY"
    ],
    "value": [
        0.5,
        20,
        400,
        0.1,
        15,
        "stripe"
    ]
})

build_material_link = pd.DataFrame({
    "build_id": ["PRINT_20260219_01"],
    "material_id": ["MAT_001"],
    "material_role": ["feedstock"]
})

build_parts = pd.DataFrame({
    "build_id": ["PRINT_20260219_01"],
    "part_id": ["PART_001"],
    "geometry_file": ["part_001.stl"],
    "layer_count": [50]
})


build_systems = pd.DataFrame({
    "build_id": ["PRINT_20260219_01"] * 6,
    "system_id": ["PF1", "PF2", "CP1", "OPT1", "MH1", "CAM_01"]
})


