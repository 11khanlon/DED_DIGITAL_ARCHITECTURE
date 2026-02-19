#%%
import numpy as np
import pandas as pd
import os

#%%
#external sensor data

melt_pool_data = pd.DataFrame({
    "parameter_name": [
        "Camera Temp(Â°F)",
        "Melt Pool Area",
        "Melt Pool Area: Valid Value"
    ]
})