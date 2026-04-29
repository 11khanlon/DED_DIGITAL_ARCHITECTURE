import numpy as np
import pandas as pd

tic_observations = pd.DataFrame({
    # identity
    "observation_id": [],

    # links to BUILD (critical CDM connection)
    "build_id": [],

    # links to SYSTEM (sensor, machine, optics, etc.)
    "system_id": [],

    # links to PROCESS vocabulary (RPM, LASER_POWER, etc.)
    "parameter_id": [],

    # time dimension
    "timestamp": [],

    # measured value (raw output)
    "value": [],

    # optional metadata (very important in real systems)
    "unit": [],
    "data_type": [],

    # quality / validity flags
    "is_valid": [],
    "quality_flag": [],

    # uncertainty / calibration context
    "measurement_error": [],
    "calibration_id": [],

    # sampling info (important for sensors like cameras / thermocouples)
    "sampling_rate_hz": [],
    "sequence_index": [],

    # source tracking (for distributed systems like yours)
    "source_system": [],
    "source_sensor": []
})


sensor_tic_metadata = pd.DataFrame({
    "system_id": [],
    "sensor_type": [],

    # optical-specific
    "resolution": [],
    "frame_rate": [],

    # thermal-specific
    "channel_id": [],

    # gas-specific
    "gas_type": [],

    # calibration
    "calibration_date": [],
    "drift_correction_factor": []
})


camera_tic = pd.DataFrame({
    "observation_id": [],
    "build_id": [],
    "system_id": ["CAM_01"],
    "parameter_id": ["MELT_POOL_AREA"],
    "timestamp": [],
    "value": [],  # float area

    # image-derived metadata
    "frame_id": [],
    "pixel_resolution": [],
    "exposure_time": [],
    "is_valid": []
})


thermocouple_tic = pd.DataFrame({
    "observation_id": [],
    "build_id": [],
    "system_id": ["TC"],
    "parameter_id": ["TEMPERATURE"],

    "timestamp": [],

    # multi-channel structure (your ch0–ch3 problem solved properly)
    "channel_id": [],
    "value": [],

    "unit": ["°F"],

    # thermal metadata
    "response_time_ms": [],
    "location": []
})



gas_sensor_tic = pd.DataFrame({
    "observation_id": [],
    "build_id": [],
    "system_id": ["O2_SENSOR", "H2O_SENSOR"],
    "parameter_id": ["OXYGEN_PPM", "HUMIDITY_PPM"],

    "timestamp": [],
    "value": [],

    "unit": ["ppm"],

    # gas-specific metadata
    "flow_condition": [],
    "sampling_mode": ["continuous", "interval"],
})


motion_tic = pd.DataFrame({
    "observation_id": [],
    "build_id": [],
    "system_id": ["MH1"],

    "parameter_id": [
        "POSITION_X",
        "POSITION_Y",
        "POSITION_Z",
        "VELOCITY_X",
        "VELOCITY_Y",
        "VELOCITY_Z"
    ],

    "timestamp": [],
    "value": [],

    "unit": ["mm", "mm/s"],

    # motion metadata
    "frame_reference": [],
    "control_mode": ["open_loop", "closed_loop"]
})

tic_quality = pd.DataFrame({
    "observation_id": [],
    "build_id": [],

    "is_valid": [],
    "quality_score": [],

    "outlier_flag": [],
    "noise_level": [],

    "missing_data_flag": [],
    "interpolation_method": []
})