#%%
import numpy as np
import pandas as pd
import os
from IPython.display import display
import xml.etree.ElementTree as ET
from graphviz import Digraph
# %%

#the parameters I use, not the names for the IDs, are directly from the RPMI source file
#in development, i will know how to strucuture this more after printing


#%%

#--Create ontology table with parameter names and descriptions--
#---machine head data---
'''
The kinematic data includes the position and velocity of the laser head. 
The position data consists of the X, Y, and Z coordinates of the laser head in inches, which indicate its location in 3D space. 
The velocity data includes the X, Y, and Z velocities of the laser head in inches per second, which describe how fast the laser head is moving along each axis. 
This information is crucial for understanding the motion of the laser during the additive manufacturing process 
and can be used to analyze the relationship between the laser's movement and the resulting melt pool characteristics.
'''
'''
machine_head_kinematic_types = pd.DataFrame({
    "kinematic_id": ["position", "velocity"],
    "subsystem_id": ["kinematic", "kinematic"],
    "description": [
        "Spatial position data",
        "Velocity data"
    ]
})'''

machine_head = pd.DataFrame({
    "machine_head_id": ["MH1"],
    "description": ["Laser machine head assembly"]
})


machine_head_features = pd.DataFrame({
    "feature_id": ["temp", "kinematic", "config"],
    "machine_head_id": ["MH1", "MH1", "MH1"],
    "description": [
        "Temperature monitoring system",
        "Motion and spatial system",
        "Operational configuration settings"
    ]
})


machine_head_temperature_data = pd.DataFrame({
    "feature_id": ["temp","temp", "temp"],
    "parameter_name": [
        "Head Temperature (RTD 1)(°F)",
        "Head Temp: Warning High Level",
        "Head Temp: Warning Low Level"
    ],
})

print(machine_head_temperature_data)

machine_head_configuration_data = pd.DataFrame({
    "feature_id": ["config"],
    "parameter_name": ["Motion Compensation Active"]
    
    
})


machine_head_kinematics = pd.DataFrame({
    "feature_id": ["kinematic", "kinematic", "kinematic"],
    "position_data": ["Pos X (inch)", "Pos Y (inch)", "Pos Z (inch)"],
    "velocity_data": ["Velocity X", "Velocity Y", "Velocity Z"]

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
    [timestamp_data, machine_head_kinematics],
    ignore_index=True
)

print(spatiotemporal_data)

#%%

#---Create XML from python---

'''
1. Create machine head parent node 
2. Create machine_head_subsystems child node 
3. Child nodes from feature_id "temp" : machine_head_temperature_data
4. Child nodes from feature id "configuration": machine_head_configuration_data
6. Child nodes from feature id kinematic "position" position_data and "velocity" machine_head_position_data

'''

root = ET.Element("MachineHead", attrib={
    "machine_head_id": "MH1",
    "description": "Laser machine head assembly"
})

#Separate machine head features
#head_subsystem_element = ET.SubElement(root, )

for index, feature_row in machine_head_features.iterrows():
    feature_element = ET.SubElement(root, "Features", 
            attrib= {
                "feature_id": feature_row["feature_id"],
                "description": feature_row["description"]
            })
    if feature_row["feature_id"] == "temp":
        for _, param_row in machine_head_temperature_data.iterrows():
            ET.SubElement(feature_element, "Parameter", attrib={
                "name": param_row["parameter_name"]
                })
    if feature_row["feature_id"] == "config":
        for _, param_row in machine_head_configuration_data.iterrows():
            ET.SubElement(feature_element, "Parameter", attrib={
                "name": param_row["parameter_name"]
                })
     # Kinematic
    elif feature_row["feature_id"] == "kinematic":
        for _, kinematic_row in machine_head_kinematics.iterrows():
            kinematic_element = ET.SubElement(feature_element, "KinematicData", attrib={
                "feature_id": kinematic_row["feature_id"],
                "position_data": kinematic_row["position_data"],
                "velocity_data": kinematic_row["velocity_data"]
            })

           
ET.indent(ET.ElementTree(root), space="  ")
output_folder = r"C:\Users\Kayleigh\DIGITAL_ARCH_REPO\RPMI_DATA_DEV\ontology_development\ontology_output"
os.makedirs(output_folder, exist_ok=True)
output_file = os.path.join(output_folder, "machine_head.xml")

tree = ET.ElementTree(root)
tree.write(output_file, encoding="utf-8", xml_declaration=True)
print("XML saved to:", output_file)

#%%
#---Create Graph---


# Load XML
tree = ET.parse(output_file)
root = tree.getroot()

dot = Digraph(comment="Machine Head System")
dot.attr(rankdir="LR")  # left-to-right layout

# Add root node
dot.node("MachineHead", "Machine Head", shape="box")

# Loop through Features
for feature in root.findall("Features"):

    feature_id = feature.attrib.get("feature_id")
    feature_description = feature.attrib.get("description")

    feature_label = f"{feature_id}\n({feature_description})"

    dot.node(feature_id, feature_label, shape="box")
    dot.edge("MachineHead", feature_id)


    # Parameters Node (diamond container)
    parameters_node_id = f"{feature_id}_Parameters"
    dot.node(parameters_node_id, "Parameters", shape="diamond")
    dot.edge(feature_id, parameters_node_id)

    # Direct Parameters
    parameters = feature.findall("Parameter")

    if parameters:
        for param in parameters:

            param_name = param.attrib.get("name")

            # Make safe node ID for Graphviz
            safe_param_id = (
                param_name.replace(" ", "_")
                .replace("(", "")
                .replace(")", "")
                .replace("/", "_")
                .replace(":", "")
                .replace("#", "")
            )

            param_node_id = f"{feature_id}_{safe_param_id}"

            dot.node(param_node_id, param_name, shape="ellipse")
            dot.edge(parameters_node_id, param_node_id)

    # Handle KinematicData (if exists)
    for kinematic in feature.findall("KinematicData"):

        kinematic_node_id = f"{feature_id}_Kinematic"
        dot.node(kinematic_node_id, "Kinematic Data", shape="diamond")
        dot.edge(feature_id, kinematic_node_id)

# Render
output_folder2 = r"C:\Users\Kayleigh\DIGITAL_ARCH_REPO\RPMI_DATA_DEV\ontology_development\ontology_output"

output_file2 = dot.render(
    filename="machine_head_er",
    directory=output_folder2,
    format="svg",
    cleanup=True
)

print("SVG generated:", output_file2)

