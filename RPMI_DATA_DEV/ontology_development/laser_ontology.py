#%%
import numpy as np
import pandas as pd
import os
from IPython.display import display
import xml.etree.ElementTree as ET
from graphviz import Digraph
#%%

#the parameters I use, not the names for the IDs, are directly from the RPMI source file

#--Optics---
optics_unit = pd.DataFrame({
    "optics_unit_id": ["OPT1"],
    "description": ["Laser optics assembly"]
})

optics_subsystems = pd.DataFrame({
    "optics_unit_id": ["OPT1"] * 6,
    "subsystem_id": [
        "laser_core",
        "cooling_system",
        "beam_monitor",
        "fiber_diagnostics",
        "optics_environment",
        "alps_positioning"
    ],
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
    alps_data], ignore_index=True)

print(all_optics_parameters)

#%%

#---Convert Python to XML---

'''#---Create unit subsystem---
Use this for later when making machine in parallel structure
for index, unit_row in optics_unit.iterrows():
    unit_element = ET.SubElement(
    root,
    "OpticsUnit",
    attrib={
        "optics_unit_id": unit_row["optics_unit_id"],
        "description": unit_row["description"]
    }
)'''

'''
1. Create parent element "Machine Optics"
2. Create opitcs subsystem element "Optics Subsystem" 
3. Match data with respective subsystem_id

'''

#---Create root---
root = ET.Element("MachineOptics") 


#Create optics subsystem
for index, subsystem_row in optics_subsystems.iterrows():

    subsystems_element = ET.SubElement(
        root, 
        "OpticsSubsystem",
        attrib={
            "optics_unit_id": subsystem_row["optics_unit_id"],
            "subsystem_id": subsystem_row["subsystem_id"],
            "description": subsystem_row["description"]
        }
    )

    parameters_element = ET.SubElement(subsystems_element, "Parameters")

    parameters_per_subsystem = all_optics_parameters[
        all_optics_parameters["subsystem_id"] == subsystem_row["subsystem_id"]
    ]

    print("Building subsystem:", subsystem_row["subsystem_id"])
    print(parameters_per_subsystem.shape)

    for index, param_row in parameters_per_subsystem.iterrows():
        ET.SubElement(
            parameters_element,
            "Parameter",
            {"name": str(param_row["parameter_name"])}
        )

# --- Generate XML string ---
tree = ET.ElementTree(root)

output_folder = r"C:\Users\Kayleigh\DIGITAL_ARCH_REPO\RPMI_DATA_DEV\ontology_development\ontology_output"
output_file = os.path.join(output_folder, "optics.xml")

# print it out nicely
ET.indent(tree, space="  ")
tree.write(output_file, encoding="utf-8", xml_declaration=True)
print("XML file created successfully.")
# %% 
# --- Create Graph ---

# Load XML
tree = ET.parse(output_file)
root = tree.getroot()

dot = Digraph(comment="Optics System")
dot.attr(rankdir="LR")  # left-to-right layout

# Add root node
dot.node("MachineOptics", "Machine Optics", shape="box")

# Loop through OpticsSubsystems
for subsystem in root.findall("OpticsSubsystem"):

    subsystem_id = subsystem.attrib.get("subsystem_id")
    subsystem_description = subsystem.attrib.get("description")

    subsystem_label = f"{subsystem_id}\n({subsystem_description})"

    dot.node(subsystem_id, subsystem_label, shape="box")
    dot.edge("MachineOptics", subsystem_id)

    # Parameters Node
    parameters_node_id = f"{subsystem_id}_Parameters"
    dot.node(parameters_node_id, "Parameters", shape="diamond")
    dot.edge(subsystem_id, parameters_node_id)

    parameters = subsystem.find("Parameters")

    if parameters is not None:
        for param in parameters.findall("Parameter"):

            param_name = param.attrib.get("name")

            # Make node id safe (Graphviz dislikes spaces & symbols)
            safe_param_id = param_name.replace(" ", "_").replace("(", "").replace(")", "").replace("/", "_")

            param_node_id = f"{subsystem_id}_{safe_param_id}"

            dot.node(param_node_id, param_name, shape="ellipse")
            dot.edge(parameters_node_id, param_node_id)

# Render
output_folder2 = r"C:\Users\Kayleigh\DIGITAL_ARCH_REPO\RPMI_DATA_DEV\ontology_development\ontology_output"

output_file2 = dot.render(
    filename="optics_er",
    directory=output_folder2,
    format="svg",
    cleanup=True
)

print("SVG generated:", output_file2)
# %%
