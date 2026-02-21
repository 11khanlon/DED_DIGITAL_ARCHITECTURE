#%%
import numpy as np
import pandas as pd
import os
#%%

internal_sensor_data = pd.DataFrame({
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