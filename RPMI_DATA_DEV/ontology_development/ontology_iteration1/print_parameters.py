#%%
import numpy as np
import pandas as pd
import os

#%%
#User input parameters related to the print process, not from RPMI data but important for the ontology

print_parameters = pd.DataFrame({
    "parameter_name": ["Build Time", "Total Layers", "Layer Height", "Travel Speed",
                        "Laser Power", "Hatch Spacing", "Energy Density", "Preheat Temperature", 
                        "Spot Size", "Scan Strategy", "Powder Feed Rate", "Stand Off Distance",
                        "Inert Gas", "Inert Gas Flow Rate", "Oxygen Level" ],
    "parameter_value": [None]*15

})