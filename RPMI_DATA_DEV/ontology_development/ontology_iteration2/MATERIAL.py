#powder and substrate

import pandas as pd
from datetime import datetime

materials = pd.DataFrame({
    "material_id": ["MAT_001", "MAT_002"],
    "material_name": ["SS 316L Powder", "SS 304L Powder"],
    "material_type": ["metal_powder", "metal_powder"],
    "supplier": ["Supplier_A", "Supplier_B"],
    "lot_number": ["LOT_316L_2026_01", "LOT_304L_2026_02"],
    "order_number": ["PO_12345", "PO_67890"],
    "form": ["powder", "powder"],
    "received_date": [datetime.now(), datetime.now()],
    "expiry_date": [None, None],
    "reuse_count": [3, 1],
    "recycled": [False, False]
})

powder_characteristics = pd.DataFrame({
    "material_id": ["MAT_001"] * 10,
    "parameter_id": [
        "PARTICLE_SIZE_D50",
        "PARTICLE_SIZE_D90",
        "MORPHOLOGY",
        "APPARENT_DENSITY",
        "TAP_DENSITY",
        "FLOWABILITY",
        "CHEMICAL_COMPOSITION",
        "OXYGEN_CONTENT",
        "MOISTURE_CONTENT",
        "MANUFACTURING_METHOD"
    ],
    "value": [
        35.0,
        55.0,
        "spherical",
        4.1,
        4.5,
        "good",
        "Fe-17Cr-12Ni-2Mo",
        0.02,
        0.01,
        "gas_atomized"
    ],
    "unit": [
        "µm", "µm", None,
        "g/cm3", "g/cm3",
        None,
        None,
        "wt%",
        "wt%",
        None
    ]
})

material_thermal_properties = pd.DataFrame({
    "material_id": ["MAT_001"] * 3,
    "parameter_id": [
        "SOLIDUS_TEMP",
        "LIQUIDUS_TEMP",
        "THERMAL_CONDUCTIVITY"
    ],
    "value": [
        1375,
        1400,
        15.0
    ],
    "unit": [
        "C",
        "C",
        "W/mK"
    ]
})

substrate_properties = pd.DataFrame({
    "material_id": ["MAT_SUB_001"],
    "parameter_id": [
        "SUBSTRATE_THICKNESS",
        "SUBSTRATE_GEOMETRY",
        "SUBSTRATE_MATERIAL",
        "SUBSTRATE_DENSITY",
        "SUBSTRATE_THERMAL_CONDUCTIVITY"
    ],
    "value": [
        10.0,
        "plate",
        "SS 316L",
        8.0,
        16.2
    ],
    "unit": [
        "mm",
        None,
        None,
        "g/cm3",
        "W/mK"
    ]
})

build_material_link = pd.DataFrame({
    "build_id": ["PRINT_20260219_01"],
    "material_id": ["MAT_001"],
    "role": ["feedstock"]
})

material_state = pd.DataFrame({
    "material_id": ["MAT_001"],
    "parameter_id": [
        "MATERIAL_TEMPERATURE",
        "OXYGEN_EXPOSURE",
        "HUMIDITY_EXPOSURE"
    ],
    "value": [
        25.0,
        50,
        40
    ],
    "unit": [
        "C",
        "ppm",
        "%"
    ]
})

material_certification = pd.DataFrame({
    "material_id": ["MAT_001"],
    "cert_id": ["CERT_316L_A1"],
    "standard": ["ASTM_F3184"],
    "tensile_strength": [580],
    "yield_strength": [290],
    "elongation": [40],
    "cert_date": [datetime.now()],
    "valid": [True]
})

MATERIAL_MODULE_EXPORTS = {
    "materials": materials,
    "powder_characteristics": powder_characteristics,
    "material_thermal_properties": material_thermal_properties,
    "substrate_properties": substrate_properties,
    "build_material_link": build_material_link,
    "material_state": material_state,
    "material_certification": material_certification
}