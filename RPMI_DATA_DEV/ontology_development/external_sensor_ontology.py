#%%
import numpy as np
import pandas as pd
import os
from IPython.display import display

#%%
#external sensor data

#maybe change to sensor_name? This framework makes it easy to add more auxiliary sensors

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

sensor_parameters = pd.DataFrame({
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
})

display(sensor_parameters)

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


sensor_data_long = pd.DataFrame({
    "sensor_id": [],
    "timestamp": [],
    "parameter_name": [],
    "value": []
})

# %%
