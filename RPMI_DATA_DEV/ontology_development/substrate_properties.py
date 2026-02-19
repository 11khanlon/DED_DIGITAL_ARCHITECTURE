
#%%
import numpy as np
import pandas as pd
import os
from IPython.display import display
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

display(substrate_properties)
# %%
