#%%
import numpy as np
import pandas as pd
import os
from IPython.display import display
import xml.etree.ElementTree as ET
from graphviz import Digraph

#%%
#--gas delivery unit data--
#lol just make a diagram in drawio
#gas_delivery_units --> hopper data --> RPM, Argon flow, Pressure, Warnings, powder data 
#                   |--> centerpurge data   
#the parameters I use, not the names for the IDs, are directly from the RPMI source file

'''
The RPMI contains 5 gas delivery units: 4 powder feeder hoppers (PF1-PF4) and 1 central purge line (CP1). 
Each unit has a unique set of parameters that are monitored during the build process.
The center purge line includes parameters related to the argon flow and pressure in the central purge line to help with print and machine protection
The four hoppers include parameters related to the powder feed rate, argon flow, and pressure for each of the four hoppers

'''

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

display(gas_delivery_units)

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
center_purge_data.insert(0, "unit_id", "CP1")



display(center_purge_data)

#also contains powder data, but its ID comes from gas delivery units...
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

hopper_data.insert(0, "unit_id", hopper_data["parameter_name"].str.extract(r"(PF\d)"))



#Create Subtables for each parameter type (RPM, Argon, Pressure, Warnings, Powder data)

RPM_data = hopper_data[hopper_data["parameter_name"].str.contains("RPM")].copy()
RPM_data.insert(1, "subsystem", "RPM")

hopper_warnings = hopper_data[hopper_data["parameter_name"].str.contains("Warning|Alarm")].copy()
hopper_warnings.insert(1, "subsystem", "Warnings")

powder_data = hopper_data[ hopper_data["parameter_name"].str.contains("Powder")].copy()
powder_data.insert(1, "subsystem", "Powder Data")

pressure_data = hopper_data[hopper_data["parameter_name"].str.contains("Pressure")].copy()
pressure_data.insert(1, "subsystem", "Pressure")

argon_data = pd.concat([hopper_data[hopper_data["parameter_name"].str.contains("Argon")], center_purge_data], ignore_index=True)
argon_data.insert(1, "subsystem", "Argon Data")

all_parameters = pd.concat([RPM_data, hopper_warnings, powder_data, pressure_data, argon_data], ignore_index=True)

print(all_parameters)


#%%

# Create the root element
root = ET.Element("GasDeliverySystem")

# --- Gas Delivery Units ---
gas_units = ET.SubElement(root, "GasDeliveryUnits")

# Define each unit
unit1 = ET.SubElement(gas_units, "Unit", attrib={"unit_id": "PF1", "unit_type": "hopper", "description": "Powder feeder hopper 1"})
unit2 = ET.SubElement(gas_units, "Unit", attrib={"unit_id": "PF2", "unit_type": "hopper", "description": "Powder feeder hopper 2"})
unit3 = ET.SubElement(gas_units, "Unit", attrib={"unit_id": "PF3", "unit_type": "hopper", "description": "Powder feeder hopper 3"})
unit4 = ET.SubElement(gas_units, "Unit", attrib={"unit_id": "PF4", "unit_type": "hopper", "description": "Powder feeder hopper 4"})
unit5 = ET.SubElement(gas_units, "Unit", attrib={"unit_id": "CP1", "unit_type": "center_purge_line", "description": "Central purge argon supply line"})

# --- Parameters for PF1 ---
pf1_params = ET.SubElement(unit1, "Parameters")
ET.SubElement(pf1_params, "Parameter", attrib={"name": "PF1 RPM"})
ET.SubElement(pf1_params, "Parameter", attrib={"name": "PF1 Argon MFlow"})
ET.SubElement(pf1_params, "Parameter", attrib={"name": "PF1 Powder Low"})
ET.SubElement(pf1_params, "Parameter", attrib={"name": "PF1 Bottom Pressure"})
ET.SubElement(pf1_params, "Parameter", attrib={"name": "PF1 Argon: Warning High Level"})

# --- Parameters for Center Purge Line ---
cp_params = ET.SubElement(unit5, "Parameters")
ET.SubElement(cp_params, "Parameter", attrib={"name": "Center Purge Argon MFlow"})
ET.SubElement(cp_params, "Parameter", attrib={"name": "Center Purge Argon: Warning High Level"})
ET.SubElement(cp_params, "Parameter", attrib={"name": "Center Purge Argon VFlow"})

# --- Generate XML string ---
tree = ET.ElementTree(root)
#tree.write("gas_delivery_ontology.xml", encoding="utf-8", xml_declaration=True)

output_folder = r"C:\Users\Kayleigh\DIGITAL_ARCH_REPO\RPMI_DATA_DEV\ontology_development\ontology_output"
output_file = f"{output_folder}\gas_delivery_ontology_pretty.xml"

# Optional: print it nicely
ET.indent(tree, space="  ")
tree.write(output_file, encoding="utf-8", xml_declaration=True)


display(tree)

#%%

# Load your XML file
tree = ET.parse("gas_delivery_ontology.xml")
root = tree.getroot()

dot = Digraph(comment="Gas Delivery System")
dot.attr(rankdir="LR")  # left to right layout

# Add system node
dot.node("GasDeliverySystem", "Gas Delivery System", shape="box")

# Loop through units
for unit in root.findall(".//Unit"):
    unit_id = unit.attrib.get("unit_id")
    unit_type = unit.attrib.get("unit_type")

    unit_label = f"{unit_id}\n({unit_type})"
    dot.node(unit_id, unit_label, shape="box")
    dot.edge("GasDeliverySystem", unit_id)

    # Add parameters
    parameters = unit.find("Parameters")
    if parameters is not None:
        for param in parameters.findall("Parameter"):
            param_name = param.attrib.get("name")
            param_id = f"{unit_id}_{param_name}"

            dot.node(param_id, param_name, shape="ellipse")
            dot.edge(unit_id, param_id)


output_folder2 = r"C:\Users\Kayleigh\DIGITAL_ARCH_REPO\RPMI_DATA_DEV\ontology_development\ontology_output"
output_file2 = f"{output_folder2}\\gas_delivery_diagram.svg"

# Render to SVG
dot.render(output_file2, format="svg", cleanup=True)

print("SVG generated: gas_delivery_diagram.svg")