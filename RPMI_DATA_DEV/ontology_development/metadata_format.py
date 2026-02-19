#%%
import numpy as np
import pandas as pd
import os
#Create metadata

print_metadata = pd.DataFrame({
    "print_id": ["PRINT_20260219_01", "PRINT_20260219_02"],
    "operator": ["Kayleigh Hanlon", "Kayleigh Hanlon"],
    "date": ["2026-02-19", "2026-02-19"],
    "material_type": ["Fe-Co Alloy", "Fe-Co Alloy"],
    "material_lot": ["LOT_12345", "LOT_12346"],
    "machine_id": ["RPMI_01", "RPMI_01"],
    "hopper_ids": ["PF1, PF2", "PF3, PF4"],
    "center_purge_unit": ["CP1", "CP1"],
    "layer_count": [50, 60],
    "layer_height": ["0.5 mm", "0.5 mm"],
    "print_speed": ["20 in/min", "18 in/min"],
    "laser_power_setpoint": [400, 420],
    "laser_power_measured": [395, 418],
    "laser_spot_size": ["0.25 in", "0.25 in"],
    "environment_conditions": ["23°C, 40% RH, 50 ppm O2", "23°C, 42% RH, 50 ppm O2"],
    "cooling_settings": ["2 L/min, 20°C", "2 L/min, 20°C"],
    "notes": ["Powder feed uneven at PF2", "No anomalies"]
})

# Print the DataFrame
print(print_metadata)