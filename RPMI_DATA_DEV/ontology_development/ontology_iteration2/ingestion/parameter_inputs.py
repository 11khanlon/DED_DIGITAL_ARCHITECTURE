import pandas as pd
import os 

toolpath_parameters = pd.DataFrame([
    {
        "parameter_id": "LASER_SPOT_SIZE",
        "value": 0.070,
        "unit": "in",
        "description": "Diameter of laser spot at focal plane"
    },
    {
        "parameter_id": "LASER_POWER",
        "value": 1070,
        "unit": "W",
        "description": "Laser output power"
    },
    {
        "parameter_id": "HEAD_TYPE",
        "value": "RPMI 45 Degree",
        "unit": None,
        "description": "Laser head configuration"
    },
    {
        "parameter_id": "NOZZLE_TYPE",
        "value": "002-0021-004 STEEP WALL",
        "unit": None,
        "description": "Powder nozzle type"
    },
    {
        "parameter_id": "NOZZLE_CHANGE_INTERVAL",
        "value": 18,
        "unit": "hr",
        "description": "Time between nozzle replacements"
    },
    {
        "parameter_id": "STANDOFF_HEIGHT",
        "value": 0.250,
        "unit": "in",
        "description": "Distance from nozzle to build surface"
    },
    {
        "parameter_id": "POWDER_FEED_RATE_IN718",
        "value": 16.00,
        "unit": "g/min",
        "description": "Powder feed rate for Inconel 718"
    },
    {
        "parameter_id": "POWDER_FEED_RATE_SS316L",
        "value": 15.20,
        "unit": "g/min",
        "description": "Powder feed rate for SS316L"
    },
    {
        "parameter_id": "LAYER_THICKNESS",
        "value": 0.015,
        "unit": "in",
        "description": "Height of each deposited layer"
    },
    {
        "parameter_id": "HATCH_WIDTH",
        "value": 0.045,
        "unit": "in",
        "description": "Distance between adjacent scan lines"
    },
    {
        "parameter_id": "HATCH_ANGLES",
        "value": "0,45,90,135,180,225,270,315",
        "unit": "deg",
        "description": "Scan rotation pattern"
    },
    {
        "parameter_id": "MODEL_OFFSET",
        "value": 0.035,
        "unit": "in",
        "description": "Geometric offset applied to toolpath"
    },
    {
        "parameter_id": "AFTER_LAYER_WAIT",
        "value": 10000,
        "unit": "ms",
        "description": "Delay between layer deposition"
    }
])




filepath = r"C:\Users\Kayleigh\DIGITAL_ARCH_REPO\RPMI_DATA_DEV\data_csv_examples"
filename = "toolpath_parameters.csv"

full_path = os.path.join(filepath, filename)

toolpath_parameters.to_csv(full_path, index=False)