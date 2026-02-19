
#%%
import numpy as np
import pandas as pd
import os
#%%

substrate_properties = pd.DataFrame({
    "parameter_name":[
        "Substrate Thickness",
        "Substrate Geometry",
        "Substrate Material",
        "Substrate Density",
        "Substrate Thermal Conductivity"],
    "parameter_value": [None]*5 
})

print(substrate_properties)
# %%
