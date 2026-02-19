# Code to generate dummy data and write it to a CSV line by line
# Simulates the data streaming from an RPMI metal powder additive machine
import csv
import time
import numpy as np
from datetime import datetime

# Set random seed for reproducibility (optional)
rng = np.random.default_rng(seed=42)

def generate_machine_data(layer_num, time_offset, x_pos, y_pos, laser_on=True):
    """
    Generate a single row of machine sensor data.
    
    Parameters:
    -----------
    layer_num : int
        Current layer number
    time_offset : float
        Time offset in seconds from start
    x_pos, y_pos : float
        Current laser position in mm
    laser_on : bool
        Whether laser is currently firing
    
    Returns:
    --------
    dict : Dictionary of sensor readings
    """
    layer_thickness = 0.8  # mm
    
    # Base parameters with noise
    laser_power = 500.0 + rng.normal(0, 10.0) if laser_on else 0.0
    scan_speed = 600.0 + rng.normal(0, 10.0) if laser_on else 0.0
    powder_flow_rate = 3.0 + rng.normal(0, 0.2)  # g/min
    oxygen_ppm = 50 + rng.normal(0, 5)
    gas_flow_rate = 30.0 + rng.normal(0, 0.5)  # L/min
    
    # Melt pool intensity depends on laser state and position
    if laser_on:
        melt_pool_intensity = 0.8 + 0.1 * np.sin(x_pos * 0.1) + rng.normal(0, 0.02)
    else:
        melt_pool_intensity = rng.normal(0.05, 0.01)  # Background noise
    
    return {
        'timestamp': datetime.now().isoformat(),
        'time_offset_s': round(time_offset, 4),
        'x_mm': round(x_pos, 4),
        'y_mm': round(y_pos, 4),
        'z_mm': round(layer_num * layer_thickness, 4),
        'powder_flow_rate_g_min': round(powder_flow_rate, 3),
        'laser_power_W': round(laser_power, 2),
        'scan_speed_mm_s': round(scan_speed, 2),
        'oxygen_ppm': round(oxygen_ppm, 1),
        'gas_flow_rate_L_min': round(gas_flow_rate, 2),
        'laser_on': int(laser_on),
        'melt_pool_intensity': round(melt_pool_intensity, 4)
    }


def write_streaming_data(output_file, num_layers=10, points_per_layer=1000, 
                         dwell=0, freq=100, build_plate_size=10):
    """
    Write dummy machine data to CSV line by line to simulate streaming.
    
    Parameters:
    -----------
    output_file : str
        Output CSV file path
    num_layers : int
        Number of layers to simulate
    points_per_layer : int
        Number of data points per layer
    delay_ms : float
        Delay between writes in milliseconds (0 for no delay)
    build_plate_size : float
        Size of build plate in mm (square)
    """
    fieldnames = [
        'timestamp', 'time_offset_s', 
        'x_mm', 'y_mm', 'z_mm',
        'powder_flow_rate_g_min', 'laser_power_W', 'scan_speed_mm_s',
        'oxygen_ppm', 'gas_flow_rate_L_min', 'laser_on', 'melt_pool_intensity'
    ]
    
    print(f"Writing streaming data to {output_file}")
    print(f"Layers: {num_layers}, Points per layer: {points_per_layer}")
    
    total_time = 0.0 # Tracker for total time
    dwell = 5.0  # seconds between layers for cooling
    dt = 1.0/freq  # Time step in seconds
    delay = dt  # delay to keep write speed in check

    with open(output_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        f.flush()
        
        for layer in range(1, num_layers + 1):
            print(f"Layer {layer}/{num_layers}...")
            
            # Generate raster scan path
            hatch_spacing = 0.5  # mm
            num_hatches = int(build_plate_size / hatch_spacing)
            points_per_hatch = points_per_layer // num_hatches
            
            for hatch in range(num_hatches):
                y_pos = hatch * hatch_spacing
                
                # Alternate scan direction (serpentine pattern)
                if hatch % 2 == 0:
                    x_positions = np.linspace(0, build_plate_size, points_per_hatch)
                else:
                    x_positions = np.linspace(build_plate_size, 0, points_per_hatch)
                
                for x_pos in x_positions:
                    start_time = time.time()
                    data = generate_machine_data(layer, total_time, x_pos, y_pos, laser_on=True)
                    writer.writerow(data)
                    
                    # Flush periodically to simulate streaming
                    if rng.random() < 0.1:
                        f.flush()
                    
                    total_time += dt
                    
                    # Dynamically adjust delay to maintain target frequency
                    elapsed_time = time.time() - start_time

                    delay = max(0, dt - elapsed_time)

                    if delay > 0:
                        time.sleep(delay)
            
            # Cooling time
            total_time += dwell
            f.flush()
    
    print(f"Done! Total time simulated: {total_time:.1f} seconds")
    print(f"Total data points: {num_layers * points_per_layer}")


if __name__ == "__main__":
    output_file = r"C:\Users\Kayleigh\DIGITAL_ARCH_REPO\RPMI_DATA_DEV\\output_files\rpmi_machine_data.csv"
    
    write_streaming_data(
        output_file=output_file,
        num_layers=5,
        points_per_layer=1000,
        freq=100,
        build_plate_size=12
    )