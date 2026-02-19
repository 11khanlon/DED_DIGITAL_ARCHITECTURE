#%%
import numpy as np
import pandas as pd
import os

#%%
#--gas delivery unit data--
#lol just make a diagram in drawio
#gas_delivery_units --> hopper data --> RPM, Argon flow, Pressure, Warnings, powder data 
#                   |--> centerpurge data   
##the parameters I use, not the names for the IDs, are directly from the RPMI source file

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
RPM_data["subsystem"] = "RPM"

hopper_warnings = hopper_data[hopper_data["parameter_name"].str.contains("Warning|Alarm")].copy()
hopper_warnings["subsystem"] = "Warnings"

powder_data = hopper_data[ hopper_data["parameter_name"].str.contains("Powder")].copy()
powder_data["subsystem"] = "Powder"

pressure_data = hopper_data[hopper_data["parameter_name"].str.contains("Pressure")].copy()
pressure_data["subsystem"] = "Pressure"

argon_data = pd.concat([hopper_data[hopper_data["parameter_name"].str.contains("Argon")],
                        center_purge_data], ignore_index=True)
argon_data["subsystem"] = "Argon Flow"

all_parameters = pd.concat([RPM_data, hopper_warnings, powder_data, pressure_data, argon_data], ignore_index=True)
