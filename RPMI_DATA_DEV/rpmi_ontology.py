#%%
import numpy as np
import pandas as pd
import os

#%%
# --- Load data ---
os.chdir(r"C:\Users\Kayleigh\DIGITAL_ARCH_REPO\RPMI_DATA_DEV")
df = pd.read_csv("dlog_2023-08-09_1106_purge testing.csv", low_memory=False)

original_shape = df.shape
print(f"Original data shape: {original_shape}")

#%%
# --- Columns to drop ---

#maybe store these in a simple file with their respective data. Do not need a relational databse

columns_to_drop = [
    "Assum Pos Z(inch)",
    "Pos Tilt",
    "Pos Rotate",
    "Pho X(inch)",
    "Pho Y(inch)",
    "Pho Z(inch)",
    "Pho Tilt",
    "Pho Rotate",
    "Velocity Tilt", #Assume rotate and tilt with their respective velocities are 0
    "Velocity Rotate", 
    "PF1 Override", , #drop redundant warnings
    "PF2 Override",
    "PF3 Override",
    "PF4 Override",
    "PF1 Argon: Warning Enabled",
    "PF1 Argon: Alarm Enabled",
    "PF1 Argon: Baseline Level",
    "PF1 Argon: Warning Tolerance Level",
    "PF1 Argon: Alarm Tolerance Level",
    "PF1 Argon: Valid Value",
    "PF2 Argon: Warning Enabled",
    "PF2 Argon: Alarm Enabled",
    "PF2 Argon: Baseline Level",
    "PF2 Argon: Alarm High Level",
    "PF1 Argon: Alarm High Level",
    "PF1 Argon: Alarm Low Level",
    "PF2 Argon: Alarm Low Level",
    "PF2 Argon: Warning Tolerance Level",
    "PF2 Argon: Alarm Tolerance Level",
    "PF2 Argon: Valid Value",
    "PF3 Argon: Warning Tolerance Level",
    "PF3 Argon: Alarm Enabled",
    "PF3 Argon: Alarm High Level",
    "PF3 Argon: Alarm Low Level",
    "PF3 Argon: Warning Tolerance Level",
    "PF3 Argon: Alarm Tolerance Level",
    "PF3 Argon: Baseline Level",
    "PF3 Argon: Valid Value",
    "PF4 Argon: Warning Enabled",
    "PF4 Argon: Alarm Enabled",
    "PF4 Argon: Baseline Level",
    "PF4 Argon: Valid Value",
    "PF4 Argon: Alarm High Level",
    "PF4 Argon: Alarm Low Level",
    "PF4 Argon: Warning Tolerance Level",
    "PF4 Argon: Alarm Tolerance Level",
    "Center Purge Argon: Warning Enabled",
    "Center Purge Argon: Alarm Enabled",
    "Center Purge Argon: Baseline Level",
    "Center Purge Argon: Valid Value",
    "Center Purge Argon: Alarm High Level",
    "Center Purge Argon: Alarm Low Level",
    "Center Purge Argon: Warning Tolerance Level",
    "Center Purge Argon: Alarm Tolerance Level",
    "Center Purge Pressure: Warning Enabled",
    "Center Purge Pressure: Alarm Enabled",
    "Center Purge Pressure: Baseline Level",
    "Center Purge Pressure: Valid Value",
    "Center Purge Pressure: Alarm High Level",
    "Center Purge Pressure: Alarm Low Level",
    "Center Purge Pressure: Warning Tolerance Level",
    "Center Purge Pressure: Alarm Tolerance Level",
    "H2O Sensor: Warning Enabled",
    "H2O Sensor: Alarm Enabled",
    "O2 Sensor: Warning Enabled",
    "O2 Sensor: Alarm Enabled",
    "O2 Sensor: Alarm High Level",
    "O2 Sensor: Alarm Low Level",
    "H2O Sensor: Alarm High Level",
    "H2O Sensor: Alarm Low Level",
    "Head Temp: Warning Enabled",
    "Head Temp: Alarm Enabled",
    "Head Temp: Alarm High Level",
    "Head Temp: Alarm Low Level",
    "PF1 Bottom Pressure: Baseline Level",
    "PF1 Bottom Pressure : Valid Value",
    "PF1 Bottom Pressure : Warning Enabled",
    "PF1 Bottom Pressure : Alarm Enabled",
    "PF1 Bottom Pressure : Alarm Tolerance Level",
    "PF1 Bottom Pressure : Alarm High Level",
    "PF1 Bottom Pressure : Alarm Low Level",
    "PF1 Bottom Pressure: Off Baseline",
    "PF1 Bottom Pressure: Warning Tolerance Level",
    "Center Purge Pressure: Warning High Level",
    "Center Purge Pressure: Warning Low Level",
    "PF2 Bottom Pressure: Baseline Level",
    "PF2 Bottom Pressure : Valid Value",
    "PF2 Bottom Pressure : Warning Enabled",
    "PF2 Bottom Pressure: Warning Tolerance Level",
    "PF2 Bottom Pressure : Warning High Level",
    "PF2 Bottom Pressure : Warning Low Level",
    "PF2 Bottom Pressure : Alarm Enabled",
    "PF2 Bottom Pressure : Alarm Tolerance Level",
    "PF2 Bottom Pressure : Alarm High Level",
    "PF2 Bottom Pressure : Alarm Low Level",
    "PF2 Bottom Pressure: Off Baseline",
    "Powder Manifold Pressure: Baseline Level",
    "Powder Manifold Pressure : Valid Value",
    "Powder Manifold Pressure : Warning Enabled",
    "Powder Manifold Pressure: Warning Tolerance Level",
    "Powder Manifold Pressure : Warning High Level",
    "Powder Manifold Pressure : Warning Low Level",
    "Powder Manifold Pressure : Alarm Enabled",
    "Powder Manifold Pressure: Alarm Tolerance Level",
    "Powder Manifold Pressure : Alarm High Level",
    "Powder Manifold Pressure : Alarm Low Level",
    "PF3 Bottom Pressure: Baseline Level",
    "PF3 Bottom Pressure : Valid Value",
    "PF3 Bottom Pressure : Warning Enabled",
    "PF3 Bottom Pressure: Warning Tolerance Level",
    "PF3 Bottom Pressure : Warning High Level",
    "PF3 Bottom Pressure : Warning Low Level",
    "PF3 Bottom Pressure : Alarm Enabled",
    "PF3 Bottom Pressure : Alarm Tolerance Level",
    "PF3 Bottom Pressure : Alarm High Level",
    "PF3 Bottom Pressure : Alarm Low Level",
    "PF3 Bottom Pressure: Off Baseline",
    "PF4 Bottom Pressure: Baseline Level",
    "PF4 Bottom Pressure : Valid Value",
    "PF4 Bottom Pressure : Warning Enabled",
    "PF4 Bottom Pressure: Warning Tolerance Level",
    "PF4 Bottom Pressure : Warning High Level",
    "PF4 Bottom Pressure : Warning Low Level",
    "PF4 Bottom Pressure : Alarm Enabled",
    "PF4 Bottom Pressure : Alarm Tolerance Level",
    "PF4 Bottom Pressure : Alarm High Level",
    "PF4 Bottom Pressure : Alarm Low Level",
    "PF4 Bottom Pressure: Off Baseline",
    "Optics Box Pressure: Baseline Level",
    "Optics Box Pressure: Valid Value",
    "Optics Box Pressure: Warning Enabled",
    "Optics Box Pressure: Warning Tolerance Level",
    "Optics Box Pressure: Warning High Level",
    "Optics Box Pressure: Warning Low Level",
    "Optics Box Pressure: Alarm Enabled",
    "Optics Box Pressure: Alarm Tolerance Level",
    "Optics Box Pressure: Alarm High Level",
    "Optics Box Pressure: Alarm Low Level",
    "Power From Meter: Warning Enabled",
    "Power From Meter: Alarm Enabled",
    "Power From Meter: Baseline Level",
    "Melt Pool Area: Warning Enabled",
    "Melt Pool Area: Warning High Level",
    "Melt Pool Area: Warning Low Level",
    "Melt Pool Area: Alarm Enabled",
    "Melt Pool Area: Alarm High Level",
    "Melt Pool Area: Alarm Low Level",
    "Melt Pool Area: Debounce Time",
    "Melt Pool Area: Baseline Level",
    "Melt Pool Area: Warning Tolerance Level",
    "Melt Pool Area: Alarm Tolerance Level",
    "Error During Execution",
    "Dryrun Mode",
    "DI Water Temp (Â°C)",
    "Cmd Mode",
    "DeadMove Override",
    "Block Number",
    "Monitoring Enabled",
    "In Warning",
    "In Alarm",
    "Events",
    "Contour Override",
    "Hatch Override"
]

#%%
# --- Filter column names ---
filtered_columns = df.drop(columns=columns_to_drop, errors='ignore').columns.tolist()
final_shape = (df.shape[0], len(filtered_columns))
print(f"Final data shape after dropping columns: {final_shape}")

#%%
# --- Create parameter table ---
parameter_table = pd.DataFrame({
    "parameter_id": range(1, len(filtered_columns) + 1),
    "parameter_name": filtered_columns
})

#%%
# --- Save to CSV ---
parameter_table.to_csv(
    "RPMI_parameter_table.csv",
    index=False
)

print("Parameter table created successfully.")

# %%
#--Create ontology table with parameter names and descriptions--

'''An ontology needs 
Hierarchy: subsystem --> parameter. create domains and subtables 
Type classification: sensor, control, state
Realtionships (measured_by_, controlled_by, part_of)
Queryable structure 
'''

kinematic_data = pd.DataFrame({
    "kinematic_id": ["position_id", "velocity_id"],
})

#tables to be stored under kinematic data
position_data = pd.DataFrame({
    "parameter_name": ["Pos X(inch)", "Pos Y(inch)", "Pos Z(inch)"],
    "description": [
        "X position of the laser head in inches",
        "Y position of the laser head in inches",
        "Z position of the laser head in inches"
    ]
})
position_data["kinematic_id"] = "position"

velocity_data = pd.DataFrame({
    "parameter_name": ["Velocity X", "Velocity Y", "Velocity Z"],    
    "description": [
        "X velocity of the laser head in inches per second",
        "Y velocity of the laser head in inches per second",
        "Z velocity of the laser head in inches per second"
    ]
})
velocity_data["kinematic_id"] = "velocity"  


'''
The kinematic data includes the position and velocity of the laser head. 
The position data consists of the X, Y, and Z coordinates of the laser head in inches, which indicate its location in 3D space. 
The velocity data includes the X, Y, and Z velocities of the laser head in inches per second, which describe how fast the laser head is moving along each axis. 
This information is crucial for understanding the motion of the laser during the additive manufacturing process 
and can be used to analyze the relationship between the laser's movement and the resulting melt pool characteristics.
'''

#Spatiotemporal data

timestamp_data = pd.DataFrame({"Layer #": "Current layer number", "TimeStamp": "Timestamp of the data point, converted to UTC"})
spatiotemporal_data = pd.DataFrame({position_data, timestamp_data})

#%%
#--Optics---
'''optics_units'''

#Laser data
laser_data = pd.DataFrame({
    "parameter_name": [
        "Laser On",
        "Pos Alps(inch)",
        "Alps Spot Size(inch)",
        "Optics Box Pressure Sensor",
        "Laser Setpoint",
        "Laser Power (from laser)",
        "Laser Water Flow (L/min)",
        "Laser Water Temp (Â°C)",
        "Laser On Time (ms)",
        "Feed Fiber FFBD (mV)",
        "Process Fiber FFBD (mV)",
        "Power From Meter",
        "Beam Size From Meter (inch)",
        "Beam Pos X From Meter (inch)",
        "Beam Pos Y From Meter (inch)",
        "Power From Meter (uncompensated)",
        "Beam Flags From Meter"
    ],
    "description": [
        "Laser On/Off status",
        "Laser position in Alps coordinate system",
        "Laser spot size in inches",
        "Pressure sensor in optics box",
        "Laser power set by the user",
        "Laser power measured from the laser source",
        "Laser cooling water flow rate",
        "Laser cooling water temperature",
        "Total laser firing time",
        "Feed fiber back reflection voltage",
        "Process fiber back reflection voltage",
        "Measured laser power from meter",
        "Measured beam size",
        "Measured beam X position",
        "Measured beam Y position",
        "Uncompensated power reading",
        "Beam status flags"
    ]
})

print(laser_data)


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

machine_head_data = pd.DataFrame({
    "parameter_name": [
        "Motion Compensation Active",
        "Head Temperature (RTD 1)(Â°F)",
        "Head Temp: Warning High Level",
        "Head Temp: Warning Low Level"
    ]
})
RPMI_machine_data = pd.DataFrame({
    "parameter_name": [
        "Box Pressure",
        "Dust Collector Diff Pressure",
        "Powder Manifold Pressure Sensor",
        "Path Setpoint Velocity(inch/min)",
        "Toolcode Execution Time"
    ]
})

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
