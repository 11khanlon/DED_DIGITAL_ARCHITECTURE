#%%
import numpy as np 
import pandas as pd 
import time
from datetime import datetime
import csv 
import os 

os.chdir(r"C:\Users\Kayleigh\DIGITAL_ARCH_REPO\RPMI_DATA_DEV")
df = pd.read_csv("dlog_2023-08-09_1106_purge testing.csv", low_memory=False)

#%%

rng = np.random.default_rng(seed=42) 
#seed = 42 you always get the same the random sequence, seed = 7 you get a different repeatable sequence


# --- Get column names and Laser on timestamp ---
columns = df.columns 
column_names1 = df.columns.tolist()
print(column_names1)
column_names = pd.Series(df.columns)
column_names.to_csv("RPMI_column_names.csv", index=False, header=False)

#%%
"create random data from parameters from the rpmi. Also generate random material data"
" Make them realistic with parameters that I have found from literature " 
#practice fetching old logic explanation. Add more variables

def generate_machine_data(layer_num, time_offset, x_pos, y_pos, laser_on = True):
    
    """
    Generate a single row of RPMI machine sensor data.
    This is machine data for a single point in the build process, with parameters that depend on the current layer, time, and laser state
    need powder flow rate
    """
    # --- Random RPMI machine parameters based on literature ---
    laser_power = 570 + rng.normal(0, 10.0) if laser_on else 0.0  # W
    spot_size = 1 + rng.normal(0, 0.1)  # mm
    scan_speed = 660 + rng.normal(0, 10.0) if laser_on else 0.0  # mm/min
    layer_thickness = 0.65 + rng.normal(0, 0.2)  # mm
    dead_move_speed = 1016 + rng.normal(0, 10.0)  # mm/min
    contour_speed = 660 + rng.normal(0, 10.0)  # mm/min
    stand_off_distance = 6 + rng.normal(0, 0.2)  # mm
    hatch_width = 0.66 + rng.normal(0, 0.1)  # mm
    oxygen_ppm = 30 + rng.normal(0, 10.0)  # ppm


    # Melt pool intensity depends on laser state and x position
    if laser_on:
        melt_pool_intensity = 0.8 + 0.1 * np.sin(x_pos * 0.1) + rng.normal(0, 0.02)
    else:
        melt_pool_intensity = rng.normal(0.05, 0.01)  # background noise

    # --- Build the data dictionary ---
    data = {
        'TimeStamp': datetime.now().isoformat(),
        'Pos X(inch)': round(x_pos / 25.4, 4),  # convert mm → inch
        'Pos Y(inch)': round(y_pos / 25.4, 4),
        'Pos Z(inch)': round(layer_num * layer_thickness / 25.4, 4),
        'Laser On': int(laser_on),
        'Laser Power (from laser)': round(laser_power, 2),
        'Laser Setpoint': round(laser_power, 2),
        'Laser On Time (ms)': round(time_offset * 1000, 2),
        'Spot Size': round(spot_size, 3),
        'Scan Speed': round(scan_speed, 2),
        'Layer #': layer_num,
        'DeadMove Override': dead_move_speed,
        'Contour Override': contour_speed,
        'Stand Off Distance': round(stand_off_distance, 2),
        'Hatch Width': round(hatch_width, 3),
        'Oxygen ppm': round(oxygen_ppm, 1),
        'Melt Pool Area': round(melt_pool_intensity, 4)
    }

    return data

#%%
def generate_sensor_data():
    temp1 = 200 + rng.normal(0,5) 
    temp2 = 200 + rng.normal(0,5) 
    temp3 = 200 + rng.normal(0,5)
    temp4 = 200 + rng.normal(0,5) 
    
#%%
def write_streaming_data(output_file, num_layers= 5, points_per_layer = 1000, freq = 1, build_plate_size = 12):
    
    """
    Write simulated RPMI machine data to CSV line by line.
    output_file = csv file name to write to 
    num_layers = number of layers to simulate 
    points_per_layer = number of data points to simulate per layer
    freq = frequency of data points in Hz (points per second)
    build_plate_size = size of the build plate in mm (assumes square)
    """

    # Only include the columns we generate
    fieldnames = [
        'TimeStamp', 'Pos X(inch)', 'Pos Y(inch)', 'Pos Z(inch)',
        'Laser On', 'Laser Power (from laser)', 'Laser Setpoint', 'Laser On Time (ms)',
        'Spot Size', 'Scan Speed', 'Layer #', 'DeadMove Override', 'Contour Override',
        'Stand Off Distance', 'Hatch Width', 'Oxygen ppm', 'Melt Pool Area'
    ]

    total_time = 0.0  # seconds, keeps track of elapsed time for timestamps
    dt = 1.0 / freq  # seconds per point
    dwell = 5.0  # cooling time between layers

    with open(output_file, 'w', newline='') as f:   #opens a csv file for writing, w = write mode, gives us a file object f, with auto closes the file
        writer = csv.DictWriter(f, fieldnames=fieldnames) #DictWriter = a csv writer that takes dictionaries instaed of lists
        writer.writeheader()  #writes column names as the first row

        #loop over layers 
        for layer in range(1, num_layers + 1):
            hatch_spacing = 0.5  # mm
            num_hatches = int(build_plate_size / hatch_spacing)  #calculate number of hatches needed to cover the build plate
            points_per_hatch = points_per_layer // num_hatches #distribute points evenly across hatches

            for hatch in range(num_hatches):
                y_pos = hatch * hatch_spacing   #y position for this hatch

                # Serpentine scan
                if hatch % 2 == 0:
                    x_positions = np.linspace(0, build_plate_size, points_per_hatch)
                else:
                    x_positions = np.linspace(build_plate_size, 0, points_per_hatch)

                for x_pos in x_positions:
                    start_time = time.time()
                    row = generate_machine_data(layer, total_time, x_pos, y_pos, laser_on=True) #generate a row of data for this point
                    writer.writerow(row)

                    total_time += dt
                    elapsed = time.time() - start_time
                    time.sleep(max(0, dt - elapsed))

            # Add dwell time after layer
            total_time += dwell

    print(f"Done! Simulated {num_layers} layers, {points_per_layer} points per layer.")


if __name__ == "__main__":
    output_file = "rpmi_machine_data.csv"
    write_streaming_data(output_file, num_layers=5, points_per_layer=1000, freq=100, build_plate_size=12)
