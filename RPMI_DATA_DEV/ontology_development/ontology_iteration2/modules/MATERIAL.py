#%%
import pandas as pd
from datetime import datetime

'''
powder and substrate, physical static properties 
static ontology model: a strucutured definition of relationships that doens't change with data 

'''

#%%

# ---------------- MATERIAL MASTER ----------------
materials = pd.DataFrame({
    "material_id": ["MAT_IN718_01"],
    "material_name": ["Inconel 718 Powder"],
    "material_type": ["metal_powder"],
    "supplier": ["Praxair"],  # example real supplier
    "lot_number": ["LOT_IN718_2026_01"],
    "batch_mass": [100.0],
    "order_number": ["PO_718_001"],
    "form": ["powder"],
    "received_date": [datetime.now()],
    "expiry_date": [None],
    "reuse_count": [2],
    "recycled": [False]
})

# ---------------- POWDER CHARACTERISTICS ----------------
powder_characteristics = pd.DataFrame({
    "material_id": ["MAT_IN718_01"] * 12,
    "parameter_id": [
        "PARTICLE_SIZE_D10",
        "PARTICLE_SIZE_D50",
        "PARTICLE_SIZE_D90",
        "MORPHOLOGY",
        "APPARENT_DENSITY",
        "TAP_DENSITY",
        "FLOWABILITY",
        "CHEMICAL_COMPOSITION",
        "OXYGEN_CONTENT",
        "NITROGEN_CONTENT",
        "MOISTURE_CONTENT",
        "MANUFACTURING_METHOD"
    ],
    "value": [
        20.0,
        35.0,
        55.0,
        "spherical",
        4.2,
        4.8,
        "good",
        "Ni-19Cr-18Fe-5Nb-3Mo-1Ti-0.5Al",
        0.015,
        0.01,
        0.005,
        "gas_atomized"
    ],
    "unit": [
        "µm", "µm", "µm",
        None,
        "g/cm3", "g/cm3",
        None,
        None,
        "wt%",
        "wt%",
        "wt%",
        None
    ]
})

# ---------------- THERMAL PROPERTIES ----------------
material_thermal_properties = pd.DataFrame({
    "material_id": ["MAT_IN718_01"] * 5,
    "parameter_id": [
        "SOLIDUS_TEMP",
        "LIQUIDUS_TEMP",
        "THERMAL_CONDUCTIVITY",
        "SPECIFIC_HEAT",
        "DENSITY"
    ],
    "value": [
        1260,
        1336,
        11.4,
        435,
        8.19
    ],
    "unit": [
        "C",
        "C",
        "W/mK",
        "J/kgK",
        "g/cm3"
    ]
})

# ---------------- SUBSTRATE ----------------
substrate_properties = pd.DataFrame({
    "material_id": ["MAT_SUB_001"] * 5,   
    "parameter_id": [
        "SUBSTRATE_THICKNESS",
        "SUBSTRATE_GEOMETRY",
        "SUBSTRATE_MATERIAL",
        "SUBSTRATE_DENSITY",
        "SUBSTRATE_THERMAL_CONDUCTIVITY"
    ],
    "value": [
        12.0,
        "plate",
        "IN718",
        8.19,
        11.4
    ],
    "unit": [
        "mm",
        None,
        None,
        "g/cm3",
        "W/mK"
    ]
})

# ---------------- BUILD LINK ----------------
build_material_link = pd.DataFrame({
    "build_id": ["PRINT_20260219_01"],
    "material_id": ["MAT_IN718_01"],
    "role": ["feedstock"]
})

# ---------------- MATERIAL STATE ----------------
material_state = pd.DataFrame({
    "material_id": ["MAT_IN718_01"] * 3,
    "parameter_id": [
        "MATERIAL_TEMPERATURE",
        "OXYGEN_EXPOSURE",
        "HUMIDITY_EXPOSURE"
    ],
    "value": [
        25.0,
        20,
        30
    ],
    "unit": [
        "C",
        "ppm",
        "%"
    ]
})

# ---------------- CERTIFICATION ----------------
material_certification = pd.DataFrame({
    "material_id": ["MAT_IN718_01"],
    "cert_id": ["CERT_IN718_A1"],
    "standard": ["AMS_5662"],   # more relevant than ASTM_F3184 here
    "tensile_strength": [1250],  # MPa
    "yield_strength": [1030],    # MPa
    "elongation": [12],          # %
    "cert_date": [datetime.now()],
    "valid": [True]
})

# ---------------- EXPORT ----------------
MATERIAL_MODULE_EXPORTS = {
    "materials": materials,
    "powder_characteristics": powder_characteristics,
    "material_thermal_properties": material_thermal_properties,
    "substrate_properties": substrate_properties,
    "build_material_link": build_material_link,
    "material_state": material_state,
    "material_certification": material_certification
}

def build_material_module():
    return MATERIAL_MODULE_EXPORTS