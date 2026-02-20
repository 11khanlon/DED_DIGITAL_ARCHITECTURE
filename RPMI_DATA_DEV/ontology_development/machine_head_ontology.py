#%%
import numpy as np
import pandas as pd
import os
# %%

#the parameters I use, not the names for the IDs, are directly from the RPMI source file

#--Create ontology table with parameter names and descriptions--

'''An ontology needs 
Hierarchy: subsystem --> parameter. create domains and subtables 
Type classification: sensor, control, state
Realtionships (measured_by_, controlled_by, part_of)
Queryable structure '''

#%%

#---machine head data---
'''
The kinematic data includes the position and velocity of the laser head. 
The position data consists of the X, Y, and Z coordinates of the laser head in inches, which indicate its location in 3D space. 
The velocity data includes the X, Y, and Z velocities of the laser head in inches per second, which describe how fast the laser head is moving along each axis. 
This information is crucial for understanding the motion of the laser during the additive manufacturing process 
and can be used to analyze the relationship between the laser's movement and the resulting melt pool characteristics.
'''

machine_head = pd.DataFrame({
    "machine_head_id": ["MH1"],
    "description": ["Laser machine head assembly"]
})


machine_head_subsystems = pd.DataFrame({
    "subsystem_id": ["temperature", "kinematic", "configuration"],
    "machine_head_id": ["MH1", "MH1", "MH1"],
    "description": [
        "Temperature monitoring system",
        "Motion and spatial system",
        "Operational configuration settings"
    ]
})


machine_head_temperature_data = pd.DataFrame({
    "parameter_name": [
        "Head Temperature (RTD 1)(°F)",
        "Head Temp: Warning High Level",
        "Head Temp: Warning Low Level"
    ],
    "subsystem_id": "temperature"
})

print(machine_head_temperature_data)

machine_head_configuration_data = pd.DataFrame({
    "parameter_name": [
        "Motion Compensation Active"
    ],
    
})

machine_head_kinematic_types = pd.DataFrame({
    "kinematic_id": ["position", "velocity"],
    "subsystem_id": ["kinematic", "kinematic"],
    "description": [
        "Spatial position data",
        "Velocity data"
    ]
})

print(machine_head_kinematic_types)

#tables to be stored under kinematic data
machine_head_position_data = pd.DataFrame({
    "parameter_name": ["Pos X (inch)", "Pos Y (inch)", "Pos Z (inch)"],
    "description": [
        "X position of the laser head in inches",
        "Y position of the laser head in inches",
        "Z position of the laser head in inches"
    ],
    "kinematic_id": "position"
})

velocity_data = pd.DataFrame({
    "parameter_name": ["Velocity X", "Velocity Y", "Velocity Z"],
    "description": [
        "X velocity of the laser head in inches per second",
        "Y velocity of the laser head in inches per second",
        "Z velocity of the laser head in inches per second"
    ],
    "kinematic_id": "velocity"
})


#%%
#Spatiotemporal data
timestamp_data = pd.DataFrame({
    "parameter_name": ["Layer #", "Timestamp"],
    "description": [
        "Current layer number",
        "Timestamp of the data point, converted to UTC"
    ],
    "subsystem_id": "kinematic"
})

#Create subtables
spatiotemporal_data = pd.concat(
    [timestamp_data, machine_head_position_data, velocity_data],
    ignore_index=True
)

print(spatiotemporal_data)