#%%
import numpy as np
import pandas as pd
import os
#%%
#--Powder Characteristics-- 
#not from RPMI data, the user must input these themselves

'''
things like powder characteristics might make sense to separate as its own material table,
since in theory you can use the same batch of powder for multiple builds/parts etc.
So then when you are doing a build you just need to link the build to the material record
Information like external factors will be heavily manual to link. "here is a spreadsheet operators add records to"

'''
powder_characteristics = pd.DataFrame({
    "parameter_name": ["Supplier, Order Number,"
    " Package Size, Material, Base_composition, Particle Size, "
    "Manufacturing Method, Morphology, Chemical Composition, Apparent density, Solidus, "
    "Liquidus, Flowwability "],
    "parameter_value": [None]*15
    
})