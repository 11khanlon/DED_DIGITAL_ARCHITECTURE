import re
import pandas as pd
from pathlib import Path



class MazakNCTraceabilityParser:
    """
    Mazak VC-500 AM .NC traceability parser

    Purpose:
    --------
    Parse Mazak additive manufacturing NC files and extract:

    - Global process parameters
    - Layer information
    - Laser ON/OFF states
    - Motion vectors
    - Feedrates
    - Tool information
    - Gas settings
    - Hopper settings
    - Coordinate transformations
    - Deposition segments

    Output:
    -------
    1. Toolpath dataframe
    2. Process parameter dataframe
    3. Vector dataframe
    4. CSV exports

    Designed to mirror the RPMI traceability pipeline structure.
    """

    def __init__(self, nc_file):
        self.nc_file = Path(nc_file)

        with open(self.nc_file, 'r', encoding='utf-8', errors='ignore') as f:
            self.lines = f.readlines()

        self.current_layer = None
        self.laser_on = False
        self.current_feed = None

        self.current_position = {
            'X': None,
            'Y': None,
            'Z': None,
            'B': None,
            'C': None
        }

        self.process_parameters = {}
        self.motion_records = []
        self.vector_records = []
        self.parameter_records = []

    # ============================================================
    # MAIN PARSER
    # ============================================================

    def parse(self):

        print("\n--- STARTING MAZAK TRACEABILITY PARSE ---")

        for line_num, raw_line in enumerate(self.lines):

            line = raw_line.strip()

            if not line:
                continue

            # ----------------------------------------------------
            # LAYER DETECTION
            # ----------------------------------------------------

            layer_match = re.search(r'\( Layer:\s*(\d+)\s*\)', line)
            if layer_match:
                self.current_layer = int(layer_match.group(1))
                print(f"Detected Layer {self.current_layer}")

            # ----------------------------------------------------
            # LASER STATE
            # ----------------------------------------------------

            if 'M438' in line:
                self.laser_on = True

            if 'M439' in line:
                self.laser_on = False

            # ----------------------------------------------------
            # FEEDRATE EXTRACTION
            # ----------------------------------------------------

            feed_match = re.search(r'F([-+]?\d*\.?\d+)', line)
            if feed_match:
                self.current_feed = float(feed_match.group(1))

            # ----------------------------------------------------
            # PROCESS PARAMETERS
            # ----------------------------------------------------

            parameter_match = re.search(
                r'#(\d+)\s*=\s*([-+]?\d*\.?\d+)',
                line
            )

            if parameter_match:
                parameter_id = int(parameter_match.group(1))
                parameter_value = float(parameter_match.group(2))

                self.process_parameters[parameter_id] = parameter_value

                self.parameter_records.append({
                    'line_number': line_num,
                    'parameter_id': parameter_id,
                    'value': parameter_value,
                    'layer': self.current_layer
                })

            # ----------------------------------------------------
            # TOOL EXTRACTION
            # ----------------------------------------------------

            tool_match = re.search(r'T(\d+)', line)
            current_tool = None

            if tool_match:
                current_tool = int(tool_match.group(1))
            else:
                current_tool = None

            # ----------------------------------------------------
            # POSITION EXTRACTION
            # ----------------------------------------------------

            updated_position = self.current_position.copy()

            for axis in ['X', 'Y', 'Z', 'B', 'C']:

                axis_match = re.search(
                    rf'{axis}([-+]?\d*\.?\d+)',
                    line
                )

                if axis_match:
                    updated_position[axis] = float(axis_match.group(1))

            # ----------------------------------------------------
            # MOTION DETECTION
            # ----------------------------------------------------

            contains_motion = any(axis in line for axis in ['X', 'Y', 'Z'])

            if contains_motion:

                record = {
                    'line_number': line_num,
                    'raw_line': line,
                    'layer': self.current_layer,
                    'laser_on': self.laser_on,
                    'feedrate': self.current_feed,
                    'tool': current_tool,
                    'X': updated_position['X'],
                    'Y': updated_position['Y'],
                    'Z': updated_position['Z'],
                    'B': updated_position['B'],
                    'C': updated_position['C']
                }

                self.motion_records.append(record)

                # Build vectors
                if len(self.motion_records) > 1:

                    prev = self.motion_records[-2]
                    curr = self.motion_records[-1]

                    self.vector_records.append({
                        'layer': curr['layer'],
                        'laser_on': curr['laser_on'],

                        'x1': prev['X'],
                        'y1': prev['Y'],
                        'z1': prev['Z'],

                        'x2': curr['X'],
                        'y2': curr['Y'],
                        'z2': curr['Z'],

                        'feedrate': curr['feedrate']
                    })

            # Update state
            self.current_position = updated_position

        print("--- PARSE COMPLETE ---\n")

    # ============================================================
    # DATAFRAME GENERATION
    # ============================================================

    def build_dataframes(self):

        self.motion_df = pd.DataFrame(self.motion_records)
        self.vector_df = pd.DataFrame(self.vector_records)
        self.parameter_df = pd.DataFrame(self.parameter_records)

        print(f"Motion records: {len(self.motion_df)}")
        print(f"Vector records: {len(self.vector_df)}")
        print(f"Parameter records: {len(self.parameter_df)}")

    # ============================================================
    # DERIVED TRACEABILITY FEATURES
    # ============================================================

    def add_derived_features(self):

        if self.motion_df.empty:
            return

        # --------------------------------------------------------
        # STEP DISTANCE
        # --------------------------------------------------------

        self.motion_df['dx'] = self.motion_df['X'].diff()
        self.motion_df['dy'] = self.motion_df['Y'].diff()
        self.motion_df['dz'] = self.motion_df['Z'].diff()

        self.motion_df['step_distance'] = (
            self.motion_df['dx']**2 +
            self.motion_df['dy']**2 +
            self.motion_df['dz']**2
        ) ** 0.5

        # --------------------------------------------------------
        # DEPOSITION FLAG
        # --------------------------------------------------------

        self.motion_df['deposition_move'] = (
            self.motion_df['laser_on'] == True
        )

        # --------------------------------------------------------
        # ESTIMATED ENERGY DENSITY
        # --------------------------------------------------------

        laser_power = self.process_parameters.get(900, None)

        if laser_power is not None:

            self.motion_df['laser_power_watts'] = laser_power

            self.motion_df['estimated_linear_energy'] = (
                laser_power /
                self.motion_df['feedrate'].replace(0, pd.NA)
            )

    # ============================================================
    # EXPORT
    # ============================================================

    def export(self, output_directory='mazak_traceability_output'):

        output_directory = Path(output_directory)
        output_directory.mkdir(exist_ok=True)

        motion_path = output_directory / 'motion_trace.csv'
        vector_path = output_directory / 'vector_trace.csv'
        parameter_path = output_directory / 'parameter_trace.csv'

        self.motion_df.to_csv(motion_path, index=False)
        self.vector_df.to_csv(vector_path, index=False)
        self.parameter_df.to_csv(parameter_path, index=False)

        print("\n--- EXPORT COMPLETE ---")
        print(f"Motion trace:    {motion_path}")
        print(f"Vector trace:    {vector_path}")
        print(f"Parameter trace: {parameter_path}")


# ================================================================
# EXECUTION
# ================================================================

if __name__ == '__main__':

    nc_file =  r"C:\\Users\\Kayleigh\\DIGITAL_ARCH_REPO\\geometry_Kay\\Boeing_testv1.nc"

    parser = MazakNCTraceabilityParser(nc_file)

    parser.parse()

    parser.build_dataframes()

    parser.add_derived_features()

    parser.export()

    print("\n--- SAMPLE MOTION DATA ---")
    print(parser.motion_df.head())

    print("\n--- SAMPLE VECTOR DATA ---")
    print(parser.vector_df.head())

    print("\n--- SAMPLE PARAMETER DATA ---")
    print(parser.parameter_df.head())


# ================================================================
# ADVANCED VECTOR ANALYTICS PIPELINE
# ================================================================

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.animation import FuncAnimation
from scipy.spatial import cKDTree


# ================================================================
# BUILD ADVANCED VECTOR DATAFRAME
# ================================================================

advanced_vector_records = []

for i in range(1, len(parser.motion_df)):

    prev_row = parser.motion_df.iloc[i - 1]
    row = parser.motion_df.iloc[i]

    advanced_vector_records.append({
        'layer': row['layer'],
        'laser_on': row['laser_on'],

        'x1': prev_row['X'],
        'y1': prev_row['Y'],
        'z1': prev_row['Z'],

        'x2': row['X'],
        'y2': row['Y'],
        'z2': row['Z'],

        'feedrate': row['feedrate'],
        'line_number': row['line_number'],
        'raw_line': row['raw_line']
    })

vectors_df = pd.DataFrame(advanced_vector_records)


# ================================================================
# GEOMETRIC METRICS
# ================================================================

vectors_df['dx'] = vectors_df['x2'] - vectors_df['x1']
vectors_df['dy'] = vectors_df['y2'] - vectors_df['y1']
vectors_df['dz'] = vectors_df['z2'] - vectors_df['z1']

vectors_df['length'] = np.sqrt(
    vectors_df['dx']**2 +
    vectors_df['dy']**2 +
    vectors_df['dz']**2
)

vectors_df['angle_deg'] = np.degrees(
    np.arctan2(vectors_df['dy'], vectors_df['dx'])
)


# ================================================================
# TURN ANGLE METRIC
# ================================================================

turn_angles = [np.nan]

for i in range(1, len(vectors_df)):

    v1 = np.array([
        vectors_df.iloc[i - 1]['dx'],
        vectors_df.iloc[i - 1]['dy']
    ])

    v2 = np.array([
        vectors_df.iloc[i]['dx'],
        vectors_df.iloc[i]['dy']
    ])

    norm1 = np.linalg.norm(v1)
    norm2 = np.linalg.norm(v2)

    if norm1 == 0 or norm2 == 0:
        turn_angles.append(np.nan)
        continue

    cos_theta = np.dot(v1, v2) / (norm1 * norm2)
    cos_theta = np.clip(cos_theta, -1, 1)

    theta = np.degrees(np.arccos(cos_theta))

    turn_angles.append(theta)

vectors_df['turn_angle_deg'] = turn_angles


# ================================================================
# TIME ESTIMATION
# ================================================================

vectors_df['feedrate_mm_sec'] = vectors_df['feedrate'] / 60.0

vectors_df['travel_time_sec'] = (
    vectors_df['length'] /
    vectors_df['feedrate_mm_sec'].replace(0, np.nan)
)

vectors_df['start_time_sec'] = (
    vectors_df['travel_time_sec']
    .cumsum()
    .shift(fill_value=0)
)

vectors_df['end_time_sec'] = (
    vectors_df['start_time_sec'] +
    vectors_df['travel_time_sec']
)


# ================================================================
# VECTOR MIDPOINTS
# ================================================================

vectors_df['xm'] = (vectors_df['x1'] + vectors_df['x2']) / 2
vectors_df['ym'] = (vectors_df['y1'] + vectors_df['y2']) / 2
vectors_df['zm'] = (vectors_df['z1'] + vectors_df['z2']) / 2




# ================================================================
# THERMAL REVISIT METRIC
# ================================================================

thermal_radius = 1.0

# initialize full column first
vectors_df['thermal_revisit_sec'] = np.nan

# keep only valid rows
valid_vectors_df = vectors_df.dropna(
    subset=['xm', 'ym', 'start_time_sec', 'end_time_sec']
).copy()

# remove inf values
finite_mask = np.isfinite(
    valid_vectors_df[['xm', 'ym']].values
).all(axis=1)

valid_vectors_df = valid_vectors_df.loc[finite_mask].copy()

# stop if empty
if len(valid_vectors_df) == 0:

    print("No valid vectors for thermal revisit analysis")

else:

    midpoints = valid_vectors_df[['xm', 'ym']].values

    kdtree = cKDTree(midpoints)

    thermal_revisit = []

    for i in range(len(valid_vectors_df)):

        current_point = midpoints[i]

        neighbors = kdtree.query_ball_point(
            current_point,
            r=thermal_radius
        )

        current_start_time = valid_vectors_df.iloc[i][
            'start_time_sec'
        ]

        previous_neighbors = [
            n for n in neighbors
            if n < i
        ]

        if len(previous_neighbors) == 0:

            thermal_revisit.append(np.nan)
            continue

        previous_times = valid_vectors_df.iloc[
            previous_neighbors
        ]['end_time_sec']

        delta_t = (
            current_start_time -
            previous_times.max()
        )

        thermal_revisit.append(delta_t)

    # assign safely
    valid_vectors_df['thermal_revisit_sec'] = thermal_revisit

    # push back into master dataframe
    vectors_df.loc[
        valid_vectors_df.index,
        'thermal_revisit_sec'
    ] = valid_vectors_df['thermal_revisit_sec']


# ================================================================
# VISUALIZATION 1
# RAW SCAN VECTORS
# ================================================================


fig, ax = plt.subplots(figsize=(10, 10))

for _, row in vectors_df.iterrows():

    ax.arrow(
        row['x1'],
        row['y1'],
        row['dx'],
        row['dy'],
        head_width=0.2,
        length_includes_head=True,
        alpha=0.7
    )

ax.set_title('Mazak Raw Scan Vectors')
ax.set_xlabel('X (mm)')
ax.set_ylabel('Y (mm)')
ax.set_aspect('equal')

plt.show()


# ================================================================
# VISUALIZATION 2
# SEQUENTIAL TOOLPATH EXECUTION
# ================================================================

fig, ax = plt.subplots(figsize=(10, 10))

segments = []

for _, row in vectors_df.iterrows():

    segments.append([
        [row['x1'], row['y1']],
        [row['x2'], row['y2']]
    ])

lc = LineCollection(
    segments,
    array=np.arange(len(segments)),
    linewidths=2
)

ax.add_collection(lc)
ax.autoscale()
ax.set_aspect('equal')

plt.colorbar(lc, label='Execution Order')

ax.set_title('Mazak Sequential Toolpath Execution')

plt.show()


# ================================================================
# VISUALIZATION 3
# LASER ON/OFF STATES
# ================================================================

fig, ax = plt.subplots(figsize=(10, 10))

for _, row in vectors_df.iterrows():

    ax.plot(
        [row['x1'], row['x2']],
        [row['y1'], row['y2']],
        color='red' if row['laser_on'] else 'gray',
        linewidth=2
    )

ax.set_title('Mazak Deposition vs Travel Moves')
ax.set_aspect('equal')

plt.show()


# ================================================================
# VISUALIZATION 4
# THERMAL REVISIT MAP
# ================================================================

fig, ax = plt.subplots(figsize=(10, 10))

scatter = ax.scatter(
    vectors_df['xm'],
    vectors_df['ym'],
    c=vectors_df['thermal_revisit_sec'],
    s=20
)

plt.colorbar(scatter, label='Thermal Revisit Time (sec)')

ax.set_title('Mazak Thermal Revisit Map')
ax.set_aspect('equal')

plt.show()


# ================================================================
# TOOLPATH REPLAY ANIMATION
# ================================================================

fig, ax = plt.subplots(figsize=(10, 10))

ax.set_xlim(
    vectors_df[['x1', 'x2']].min().min() - 1,
    vectors_df[['x1', 'x2']].max().max() + 1
)

ax.set_ylim(
    vectors_df[['y1', 'y2']].min().min() - 1,
    vectors_df[['y1', 'y2']].max().max() + 1
)

ax.set_aspect('equal')


def animate(i):

    ax.clear()

    subset = vectors_df.iloc[:i]

    for _, row in subset.iterrows():

        ax.plot(
            [row['x1'], row['x2']],
            [row['y1'], row['y2']],
            color='red' if row['laser_on'] else 'gray'
        )

    ax.set_title(f'Mazak Toolpath Replay: Step {i}')
    ax.set_aspect('equal')


ani = FuncAnimation(
    fig,
    animate,
    frames=len(vectors_df),
    interval=1
)

plt.show()


# ================================================================
# EXPORT ADVANCED VECTOR DATASET
# ================================================================

vectors_df.to_csv(
    'mazak_vectors_advanced.csv',
    index=False
)

print('Saved vector dataset: mazak_vectors_advanced.csv')


# ================================================================
# SUMMARY STATISTICS
# ================================================================

print('MAZAK SUMMARY')

print(f'Total vectors: {len(vectors_df)}')
print(f'Total deposition distance: {vectors_df["length"].sum():.2f} mm')
print(f'Total build time estimate: {vectors_df["travel_time_sec"].sum()/60:.2f} minutes')
print(f'Mean vector length: {vectors_df["length"].mean():.3f} mm')
print(f'Mean thermal revisit: {vectors_df["thermal_revisit_sec"].mean():.2f} sec')


# ================================================================
# IMPORTANT MAZAK PARAMETERS
# ================================================================

"""
#900 = Laser Power [W]
#901 = Nozzle Gas [L/min]
#902 = Shield Gas [L/min]
#903 = Disk 1 Speed [%]
#904 = Carrier Gas 1 [L/min]
#905 = Disk 2 Speed [%]
#906 = Carrier Gas 2 [L/min]
#907 = Hopper Selection
#911 = Laser State

M438 = Laser ON
M439 = Laser OFF
M440 = Nozzle Gas ON
M441 = Shield Gas ON
G68.2 = Coordinate Transformation
G43.4 = TCP Tool Compensation
G53.1 = Tilted Work Plane
"""