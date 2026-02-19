#%%
import numpy as np
import pandas as pd
import os
#%%

#the parameters I use, not the names for the IDs, are directly from the RPMI source file

#--Optics---
optics_unit = pd.DataFrame({
    "optics_unit_id": ["OPT1"],
    "description": ["Laser optics assembly"]
})

optics_subsystems = pd.DataFrame({
    "subsystem_id": [
        "laser_core",
        "cooling_system",
        "beam_monitor",
        "fiber_diagnostics",
        "optics_environment",
        "alps_positioning"
    ],
    "optics_unit_id": ["OPT1"] * 6,
    "description": [
        "Laser emission and control",
        "Laser cooling and water system",
        "Beam measurement and metrology",
        "Fiber back reflection diagnostics",
        "Optics enclosure environmental monitoring",
        "ALPS beam positioning system"
    ]
})

laser_core_data = pd.DataFrame({
    "parameter_name": [
        "Laser On",
        "Laser Setpoint",
        "Laser Power (from laser)",
        "Laser On Time (ms)"
    ],
    "subsystem_id": "laser_core"
})

cooling_data = pd.DataFrame({
    "parameter_name": [
        "Laser Water Flow (L/min)",
        "Laser Water Temp (°C)"
    ],
    "subsystem_id": "cooling_system"
})

beam_monitor_data = pd.DataFrame({
    "parameter_name": [
        "Power From Meter",
        "Power From Meter (uncompensated)",
        "Beam Size From Meter (inch)",
        "Beam Pos X From Meter (inch)",
        "Beam Pos Y From Meter (inch)",
        "Beam Flags From Meter"
    ],
    "subsystem_id": "beam_monitor"
})

fiber_diagnostics_data = pd.DataFrame({
    "parameter_name": [
        "Feed Fiber FFBD (mV)",
        "Process Fiber FFBD (mV)"
    ],
    "subsystem_id": "fiber_diagnostics"
})

optics_environment_data = pd.DataFrame({
    "parameter_name": [
        "Optics Box Pressure Sensor"
    ],
    "subsystem_id": "optics_environment"
})

alps_data = pd.DataFrame({
    "parameter_name": [
        "Pos Alps (inch)",
        "Alps Spot Size (inch)"
    ],
    "subsystem_id": "alps_positioning"
})


all_optics_parameters = pd.concat([
    laser_core_data,
    cooling_data,
    beam_monitor_data,
    fiber_diagnostics_data,
    optics_environment_data,
    alps_data], ignore_index=True)