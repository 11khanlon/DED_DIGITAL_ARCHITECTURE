import numpy as np 
import pandas as pd 

'''
 AM-CDD aligned vocab
 This is what the machine is doing 
 RPM, Argon flow, pressure, laser power
'''

process_parameters = pd.DataFrame({
    "parameter_id": [
        # Feeder / Hopper
        "RPM",
        "RPM_SETPOINT",
        "POWDER_FEED_RATE",
        "POWDER_LOW_LEVEL",
        "ALARM_ENABLED",

        # Gas Delivery
        "ARGON_MFLOW",
        "ARGON_VFLOW",
        "ARGON_FLOW",
        "ARGON_TEMP",
        "PRESSURE",
        "PRESSURE_TOP",
        "PRESSURE_BOTTOM",

        # Laser / Optics
        "LASER_POWER",
        "LASER_POWER_SETPOINT",
        "LASER_ON_TIME",
        "SCAN_SPEED",
        "BEAM_SIZE",
        "BEAM_POSITION_X",
        "BEAM_POSITION_Y",

        # Thermal / Cooling
        "COOLING_FLOW",
        "COOLING_TEMPERATURE",

        # Build / Print Process
        "LAYER_HEIGHT",
        "HATCH_SPACING",
        "ENERGY_DENSITY",
        "PRINT_SPEED",

        # Motion / Machine Head
        "MOTION_COMPENSATION",
        "POSITION_X",
        "POSITION_Y",
        "POSITION_Z",
        "VELOCITY_X",
        "VELOCITY_Y",
        "VELOCITY_Z"
    ],

    "description": [
        # Feeder
        "Rotational speed of powder feeder",
        "Target RPM setpoint for feeder control",
        "Rate of powder delivery",
        "Low powder threshold indicator",
        "Alarm enable/disable flag",

        # Gas
        "Mass flow of argon gas",
        "Volumetric flow of argon gas",
        "General argon flow rate",
        "Temperature of argon gas",
        "System pressure",
        "Upper pressure measurement",
        "Lower pressure measurement",

        # Laser / Optics
        "Laser output power",
        "Laser power setpoint",
        "Laser active emission time",
        "Scan velocity of laser beam",
        "Laser beam diameter",
        "Beam X position",
        "Beam Y position",

        # Cooling
        "Cooling fluid flow rate",
        "Cooling system temperature",

        # Build process
        "Thickness of each deposited layer",
        "Spacing between scan paths",
        "Energy delivered per unit area",
        "Overall print scan speed",

        # Motion
        "Motion compensation enable flag",
        "Machine head X position",
        "Machine head Y position",
        "Machine head Z position",
        "Velocity along X axis",
        "Velocity along Y axis",
        "Velocity along Z axis"
    ],

    "unit": [
        # Feeder
        "rpm",
        "rpm",
        "g/min",
        "bool",
        "bool",

        # Gas
        "g/s",
        "L/min",
        "L/min",
        "°F",
        "psi",
        "psi",
        "psi",

        # Laser / Optics
        "W",
        "W",
        "ms",
        "mm/s",
        "mm",
        "mm",
        "mm",

        # Cooling
        "L/min",
        "°C",

        # Build
        "mm",
        "mm",
        "J/mm^2",
        "mm/s",

        # Motion
        "bool",
        "mm",
        "mm",
        "mm",
        "mm/s",
        "mm/s",
        "mm/s"
    ]
})

print(process_parameters)