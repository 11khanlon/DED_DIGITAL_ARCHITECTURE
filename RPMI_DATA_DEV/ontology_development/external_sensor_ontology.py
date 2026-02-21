#%%
import numpy as np
import pandas as pd
import os
from IPython.display import display
import xml.etree.ElementTree as ET
from graphviz import Digraph

#%%
#external sensor data

#maybe change to sensor_name? This framework makes it easy to add more auxiliary sensors

'''
The printing process is monitored by two external sensors: a melt pool monitoring camera and a thermocouple array
These sensors have certain characteritics that should be noted before printing to understand the data they produce
Each sensor produces a unique set of parameters that are monitored during the build process. These paraemters are either bool, float or datetime data types.

'''
'''
This structure has a sensor ID to identify everything. 
each attribute is a column after the sensor id 
so far this one is the best structured

'''

#Eventually create on big sensor table with the external sensors being a child to entity SENSOR
#%%

external_sensors = pd.DataFrame({
    "sensor_id": ["CAM_01", "TC"],
    "sensor_type": ["optical_camera", "thermocouple"],
    "description": [
        "Melt pool monitoring camera",
        "K-type thermocouple array"
    ]
})

display(external_sensors)

sensor_characteristics = pd.DataFrame({
    "sensor_id": ["CAM_01", "TC"],
    "model": ["FLIR A35", "Omega K-Type"],
    "placement": ["Coaxial with laser", "Build plate underside"],
    "sampling_frequency_hz": [1000, 10],  #example values
    "measurement_units": ["pixels / °F", "°F"],
    "calibration_date": ["2026-01-15", "2026-01-10"],
    "error_metric": ["±2%", "±1.5°F"]
})

display(sensor_characteristics)

'''sensor_parameters = pd.DataFrame({
    "sensor_id": [
        "CAM_01", "CAM_01", "CAM_01",
        "TC", "TC", "TC", "TC", "TC"
    ],
    "parameter_name": [
        "camera_temp_F",
        "melt_pool_area",
        "melt_pool_area_valid",
        "timestamp",
        "ch0",
        "ch1",
        "ch2",
        "ch3"
    ],
    "data_type": [
        "float", "float", "bool",
        "datetime", "float", "float", "float", "float"
    ]
})'''


melt_pool_data = pd.DataFrame({
    "sensor_id": "CAM_01",
    "timestamp": pd.to_datetime([
        "2026-02-19 12:00:00",
        "2026-02-19 12:00:01"
    ]),
    "camera_temp_F": [120.5, 121.0],
    "melt_pool_area": [3.45, 3.51],
    "melt_pool_area_valid": [True, True]
})

display(melt_pool_data)

thermocouple_data = pd.DataFrame({
    "sensor_id": "TC",
    "timestamp": pd.to_datetime([
        "2026-02-19 12:00:00",
        "2026-02-19 12:00:01"
    ]),
    "ch0": [450.1, 451.0],
    "ch1": [449.8, 450.5],
    "ch2": [452.3, 453.0],
    "ch3": [448.9, 449.2]
})

display(thermocouple_data)


sensor_data_log = pd.DataFrame({
    "sensor_id": [],
    "timestamp": [],
    "parameter_name": [],
    "value": []
})

display(sensor_data_log)

# %%

#---Create XML structure based on python tables---

'''
1. Loop through each sensor 
2. Create XML <Sensor> node 
3. Adding <characteristics> (metadata) and <data> (time series records)
'''

# Create root
root = ET.Element("ExternalSensors")

# Loop through each sensor in registry
for index, sensor_row in external_sensors.iterrows():

    # Create Sensor node
    sensor_element = ET.SubElement(
        root,
        "Sensor",
        attrib={
            "sensor_id": sensor_row["sensor_id"],
            "sensor_type": sensor_row["sensor_type"],
            "description": sensor_row["description"]
        }
    )

    # Add Characteristics (parent, create new sub-element name)
    characteristics_element = ET.SubElement(sensor_element, "Characteristics")

    # Filter characteristics table for this sensor
    sensor_char = sensor_characteristics[
        sensor_characteristics["sensor_id"] == sensor_row["sensor_id"]
    ]

    for index, char_row in sensor_char.iterrows():
        for col in sensor_char.columns:
            if col != "sensor_id":
                ET.SubElement(
                    characteristics_element,
                    col
                ).text = str(char_row[col])

    '''iterate row by row in that filtered table, then loop over each column to avoid "sensor_id"
    The ET SubElement creates the XML tags. (subelement, col) col stands for index in the column
    col = "type" 
    char_row[col] = "optical"
    '''

    # Add Data  (parent, create new sub-element name)
    data_element = ET.SubElement(sensor_element, "Data")

    # Select correct data table
    if sensor_row["sensor_id"] == "CAM_01":
        data_df = melt_pool_data
    elif sensor_row["sensor_id"] == "TC":
        data_df = thermocouple_data
    else:
        data_df = None

    if data_df is not None:
        for index, data_row in data_df.iterrows():
            record = ET.SubElement(data_element, "Record")

            for col in data_df.columns:
                ET.SubElement(
                    record,
                    col
                ).text = str(data_row[col])


# --- Generate XML string ---
tree = ET.ElementTree(root)

output_folder = r"C:\Users\Kayleigh\DIGITAL_ARCH_REPO\RPMI_DATA_DEV\ontology_development\ontology_output"
output_file = os.path.join(output_folder, "external_sensors.xml")

# print it out nicely
ET.indent(tree, space="  ")
tree.write(output_file, encoding="utf-8", xml_declaration=True)
print("XML file created successfully.")

#%%

#---Create Graph---

# Load XML
tree = ET.parse(output_file)  # use your output file name
root = tree.getroot()

dot = Digraph(comment="External Sensors System")
dot.attr(rankdir="LR")  # left-to-right layout

# Add root node
dot.node("ExternalSensors", "External Sensors", shape="box")

# Loop through Sensors
for sensor in root.findall("Sensor"):

    sensor_id = sensor.attrib.get("sensor_id")
    sensor_type = sensor.attrib.get("sensor_type")

    sensor_label = f"{sensor_id}\n({sensor_type})"
    dot.node(sensor_id, sensor_label, shape="box")
    dot.edge("ExternalSensors", sensor_id)

   
    # Characteristics Node
    char_node_id = f"{sensor_id}_Characteristics"
    dot.node(char_node_id, "Characteristics", shape="diamond")
    dot.edge(sensor_id, char_node_id)

    characteristics = sensor.find("Characteristics")
    if characteristics is not None:
        for element in characteristics:
            param_node_id = f"{sensor_id}_{element.tag}"
            dot.node(param_node_id, element.tag, shape="ellipse")
            dot.edge(char_node_id, param_node_id)

    # Data Node
    data_node_id = f"{sensor_id}_Data"
    dot.node(data_node_id, "Data", shape="diamond")
    dot.edge(sensor_id, data_node_id)

    data = sensor.find("Data")
    if data is not None:

        # Get first record only to extract schema (avoid plotting every timestamp)
        first_record = data.find("Record")

        if first_record is not None:
            for element in first_record:
                param_node_id = f"{sensor_id}_data_{element.tag}"
                dot.node(param_node_id, element.tag, shape="ellipse")
                dot.edge(data_node_id, param_node_id)


# Render
dot.render("external_sensors_er", format="svg", cleanup=True)
output_file2 = os.path.join(output_folder, "external_sensors_er" )

print("SVG generated: external_sensors_er.svg")

# %%
