#%%
import numpy as np
import pandas as pd
import os
# %%
#--Create ontology table with parameter names and descriptions--

'''An ontology needs 
Hierarchy: subsystem --> parameter. create domains and subtables 
Type classification: sensor, control, state
Realtionships (measured_by_, controlled_by, part_of)
Queryable structure 
'''

#%%

RPMI_machine_data = pd.DataFrame({
    "parameter_name": [
        "Box Pressure",
        "Dust Collector Diff Pressure",
        "Powder Manifold Pressure Sensor",
        "Path Setpoint Velocity(inch/min)",
        "Toolcode Execution Time"
    ]
})

''' variables that are helpful for RPMI, but I won't know until I print'''
   
#%%

#---machine head data---

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


'''
The kinematic data includes the position and velocity of the laser head. 
The position data consists of the X, Y, and Z coordinates of the laser head in inches, which indicate its location in 3D space. 
The velocity data includes the X, Y, and Z velocities of the laser head in inches per second, which describe how fast the laser head is moving along each axis. 
This information is crucial for understanding the motion of the laser during the additive manufacturing process 
and can be used to analyze the relationship between the laser's movement and the resulting melt pool characteristics.
'''
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

#overlapping x data with kinematic data though

#%%
#--Optics---


optics_unit = pd.DataFrame({
    "optics_unit_id": ["OPT1"],
    "description": ["Laser optics assembly"]
})

optics_subsystems = pd.DataFrame({
    "subsystem_id": [
        "laser_core",
        "cooling_system",
        "beam_monitor",
        "fiber_diagnostics",
        "optics_environment",
        "alps_positioning"
    ],
    "optics_unit_id": ["OPT1"] * 6,
    "description": [
        "Laser emission and control",
        "Laser cooling and water system",
        "Beam measurement and metrology",
        "Fiber back reflection diagnostics",
        "Optics enclosure environmental monitoring",
        "ALPS beam positioning system"
    ]
})

laser_core_data = pd.DataFrame({
    "parameter_name": [
        "Laser On",
        "Laser Setpoint",
        "Laser Power (from laser)",
        "Laser On Time (ms)"
    ],
    "subsystem_id": "laser_core"
})

cooling_data = pd.DataFrame({
    "parameter_name": [
        "Laser Water Flow (L/min)",
        "Laser Water Temp (°C)"
    ],
    "subsystem_id": "cooling_system"
})

beam_monitor_data = pd.DataFrame({
    "parameter_name": [
        "Power From Meter",
        "Power From Meter (uncompensated)",
        "Beam Size From Meter (inch)",
        "Beam Pos X From Meter (inch)",
        "Beam Pos Y From Meter (inch)",
        "Beam Flags From Meter"
    ],
    "subsystem_id": "beam_monitor"
})

fiber_diagnostics_data = pd.DataFrame({
    "parameter_name": [
        "Feed Fiber FFBD (mV)",
        "Process Fiber FFBD (mV)"
    ],
    "subsystem_id": "fiber_diagnostics"
})

optics_environment_data = pd.DataFrame({
    "parameter_name": [
        "Optics Box Pressure Sensor"
    ],
    "subsystem_id": "optics_environment"
})

alps_data = pd.DataFrame({
    "parameter_name": [
        "Pos Alps (inch)",
        "Alps Spot Size (inch)"
    ],
    "subsystem_id": "alps_positioning"
})


all_optics_parameters = pd.concat([
    laser_core_data,
    cooling_data,
    beam_monitor_data,
    fiber_diagnostics_data,
    optics_environment_data,
    alps_data
], ignore_index=True)



#%%
#--gas delivery unit data--
#lol just make a diagram in drawio
#gas_delivery_units --> hopper data --> RPM, Argon flow, Pressure, Warnings, powder data 
#                   |--> centerpurge data   

gas_delivery_units = pd.DataFrame({
    "unit_id": ["PF1", "PF2", "PF3", "PF4", "CP1"],
    "unit_type": [
        "hopper",
        "hopper",
        "hopper",
        "hopper",
        "center_purge_line"
    ],
    "description": [
        "Powder feeder hopper 1",
        "Powder feeder hopper 2",
        "Powder feeder hopper 3",
        "Powder feeder hopper 4",
        "Central purge argon supply line"
    ]
})


center_purge_data = pd.DataFrame({
    "parameter_name": [
        "Center Purge Argon MFlow",
        "Center Purge Argon: Warning High Level",
        "Center Purge Argon: Warning Low Level",
        "Center Purge Argon VFlow",
        "Center Purge Argon Temp(Â°F)",
        "Center Purge Argon Absolute Pressure"
    ]
})

center_purge_data["unit_id"] = "CP1"
'''
df["column_name"] access the a column
so center_purge_data["unit_id"] will access column unit_id inside center_purge_data 
but this column does not exist yet, so pandas will create it 

'''

#Single Child table
hopper_data = pd.DataFrame({
    "parameter_name": [

        #PF1 parameters
        "PF1 RPM",
        "PF1 RPM Setpoint",
        "PF1 Argon MFlow",
        "PF1 Argon: Warning High Level",
        "PF1 Argon: Warning Low Level",
        "PF1 Argon VFlow",
        "PF1 Argon Temp(Â°F)",
        "PF1 Argon Absolute Pressure",
        "PF1 Powder Low",
        "PF1 Powder Low: Warning Enabled",
        "PF1 Powder Low: Alarm Enabled",
        "PF1 Top Pressure",
        "PF1 Bottom Pressure",
        "PF1 Bottom Pressure : Warning High Level",
        "PF1 Bottom Pressure : Warning Low Level"
         
        #RF2 parameters
        "PF2 RPM",
        "PF2 RPM Setpoint",
        "PF2 Argon MFlow",
        "PF2 Argon: Warning High Level",
        "PF2 Argon: Warning Low Level",
        "PF2 Argon VFlow",
        "PF2 Argon Temp(Â°F)",
        "PF2 Argon Absolute Pressure",
        "PF2 Powder Low",
        "PF2 Powder Low: Warning Enabled",
        "PF2 Powder Low: Alarm Enabled",
        "PF2 Top Pressure",
        "PF2 Bottom Pressure",
        "PF2 Bottom Pressure : Warning High Level",
        "PF2 Bottom Pressure : Warning Low Level"
        
        #PF3 parameters
        "PF3 RPM",
        "PF3 RPM Setpoint",
        "PF3 Argon MFlow",
        "PF3 Argon: Warning High Level",
        "PF3 Argon: Warning Low Level",
        "PF3 Argon VFlow",
        "PF3 Argon Temp(Â°F)",
        "PF3 Argon Absolute Pressure",
        "PF3 Powder Low",
        "PF3 Powder Low: Warning Enabled",
        "PF3 Powder Low: Alarm Enabled",
        "PF3 Top Pressure",
        "PF3 Bottom Pressure",
        "PF3 Bottom Pressure : Warning High Level",
        "PF3 Bottom Pressure : Warning Low Level"

        #PF4 parameters
        "PF4 RPM",
        "PF4 RPM Setpoint",
        "PF4 Argon MFlow",
        "PF4 Argon: Warning High Level",
        "PF4 Argon: Warning Low Level",
        "PF4 Argon VFlow",
        "PF4 Argon Temp(Â°F)",
        "PF4 Argon Absolute Pressure",
        "PF4 Powder Low",
        "PF4 Powder Low: Warning Enabled",
        "PF4 Powder Low: Alarm Enabled",
        "PF4 Top Pressure",
        "PF4 Bottom Pressure",
        "PF4 Bottom Pressure : Warning High Level",
        "PF4 Bottom Pressure : Warning Low Level"
          ]
})
hopper_data["unit_id"] = hopper_data["parameter_name"].str.extract(r"(PF\d)")


'''
Pandas syntax:
The pandas code is doing boolean filering, not an index lookup.
PF_data["parameter_name"] returns a series of all the parameter names in that table. 
series.str --> pandas string accessor. It allows you to apply string operations to an entire column of a DataFrame
.str means apply string operations to each element in the series 
.str.contains("RPM") searches each string and will return only rows where the condition is true or RPM is found

So instead of, give me item at index 0. Give me all rows where this condition is True
df[df["col"].str.contains("x")]

'''


#Create Subtables for each parameter type (RPM, Argon, Pressure, Warnings, Powder data)

RPM_data = hopper_data[hopper_data["parameter_name"].str.contains("RPM")].copy()

hopper_warnings = hopper_data[hopper_data["parameter_name"].str.contains("Warning|Alarm")].copy()

powder_data = hopper_data[ hopper_data["parameter_name"].str.contains("Powder")].copy()

pressure_data = hopper_data[hopper_data["parameter_name"].str.contains("Pressure")].copy()

argon_data = pd.concat([hopper_data[hopper_data["parameter_name"].str.contains("Argon")],
                        center_purge_data], ignore_index=True)



#%%
#external sensor data

melt_pool_data = pd.DataFrame({
    "parameter_name": [
        "Camera Temp(Â°F)",
        "Melt Pool Area",
        "Melt Pool Area: Valid Value"
    ]
})
#%%

RPMI_sensor_data = pd.DataFrame({
    "sensor_id": ["H2O Sensor", "O2 Sensor"]

})

H20_Sensor_data = pd.DataFrame({
    "parameter_name": [
        "H2O Sensor",
        "H2O Sensor: Warning High Level",
        "H2O Sensor: Warning Low Level"
    ]
})
H20_Sensor_data["sensor_id"] = "H2O Sensor"

O2_Sensor_data = pd.DataFrame({
    "parameter_name": [
        "O2 Sensor",
        "O2 Sensor: Warning High Level",
        "O2 Sensor: Warning Low Level"
    ]
})
O2_Sensor_data["sensor_id"] = "O2 Sensor"



#%%
#--Powder Characteristics-- 

'''
things like powder characteristics might make sense to separate as its own material table,
since in theory you can use the same batch of powder for multiple builds/parts etc.
So then when you are doing a build you just need to link the build to the material record
Information like external factors will be heavily manual to link. "here is a spreadsheet operators add records to"

'''
powder_characteristics = pd.DataFrame({
    "parameter_name": []

})

#%%

print_parameters = pd.DataFrame({


})

#%%

substrate_properties = pd.DataFrame({
    "parameter_name": [
        "Substrate Thickness",
        "Substrate Geometry",
        "Substrate Material",
        "Substrate Density",
        "Substrate Thermal Conductivity",
    ]
})

#%%
