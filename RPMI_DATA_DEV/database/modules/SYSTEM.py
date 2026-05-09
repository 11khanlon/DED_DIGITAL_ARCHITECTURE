#%%
import pandas as pd

#%%
def build_system_module():

    am_system = pd.DataFrame({
        "machine_id": ["RPMI_01"],
        "system_name": ["RPMI DED Machine"],
        "process_type": ["directed_energy_deposition"],
        "location": ["Lab_A"],
        "manufacturer": ["RPMI"],
        "model": ["RPMI-DED-45"],
        "build_volume_x_mm": [300],
        "build_volume_y_mm": [300],
        "build_volume_z_mm": [400],
        "last_calibration_date": [None],
        "maintenance_date": [None]
    })

    systems = pd.DataFrame({
        "system_id": [
            "RPMI_01",
            "PF1", "PF2", "PF3", "PF4",
            "CP1",
            "LASER_01",
            "MH1",
            "CAM_01",
            "TC",
            "O2_SENSOR",
            "H2O_SENSOR"
        ],
        "system_type": [
            "machine",
            "hopper", "hopper", "hopper", "hopper",
            "purge_line",
            "laser",
            "machine_head",
            "camera",
            "thermocouple",
            "gas_sensor",
            "gas_sensor"
        ],
        "parent_system": [
            None,
            "RPMI_01", "RPMI_01", "RPMI_01", "RPMI_01",
            "RPMI_01",
            "RPMI_01",
            "RPMI_01",
            "RPMI_01",
            "MH1",
            "RPMI_01",
            "RPMI_01"
        ]
    })

    return {
        "am_system": am_system,
        "systems": systems
    }


