# RPMI MPF Spatiotemporal Manufacturing Analysis Pipeline

#%%
"""
RPMI MPF TOOLPATH ANALYSIS PIPELINE

1. Parses RPMI .mpf files
2. Extracts manufacturing states
3. Reconstructs deposition vectors
4. Computes geometric metrics
5. Estimates timestamps
6. Computes thermal revisit metrics
7. Visualizes:
    - scan vectors
    - contour vs hatch
    - sequential execution
    - thermal accumulation

"""

#%%
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.animation import FuncAnimation
from scipy.spatial import cKDTree
from mpl_toolkits.mplot3d import Axes3D
from scipy.spatial import ConvexHull

#%%
''''
Laser spot size = 0.070 inches 
laser power range = 1070 W 
head type = 45 degree 
standoff distance = 0.25 
powder feed rate = 16 (IN 718)
layer thickness = 0.015 
hatch width = 0.045 
after layer wait = 10000 ms 
hatch angles = every 45 degrees

'''

#%%
# USER INPUT

mpf_path = r"C:\\Users\\Kayleigh\\DIGITAL_ARCH_REPO\\geometry_Kay\\PartGeometry_nostock_drill.mpf"

# thermal neighborhood radius (inches)
thermal_radius = 0.10

#%%
# LOAD MPF
with open(mpf_path, 'r') as f:
    lines = f.readlines()

print(f"Loaded {len(lines)} MPF lines")

#%%
# REGEX PATTERNS

line_number_pattern = re.compile(r'N(\d+)')

xyz_pattern = re.compile(
    r'X=([-\d\.]+)\s*Y=([-\d\.]+)\s*Z=([-\d\.]+)'
)

feed_pattern = re.compile(r'F=([-\d\.]+)')

power_pattern = re.compile(r'M54=([-\d\.]+)')

mode_pattern = re.compile(r'\$A_DBB\[88\]=(\d+)')

layer_pattern = re.compile(r'Start of Layer:(\d+)')

#%%
# STATE VARIABLES

current_mode = 'UNKNOWN'
current_feedrate = np.nan
current_power = np.nan
current_layer = 0

mode_lookup = {
    '1': 'CONTOUR',
    '2': 'HATCH',
    '3': 'OTHER'
}

#%%
# EXTRACT EVENTS

records = []

for raw_line in lines:

    line = raw_line.strip()

    # line number
    line_match = line_number_pattern.search(line)
    if line_match:
        line_number = int(line_match.group(1))
    else:
        line_number = -1

    # layer
    layer_match = layer_pattern.search(line)
    if layer_match:
        current_layer = int(layer_match.group(1))

    # mode
    mode_match = mode_pattern.search(line)
    if mode_match:
        mode_code = mode_match.group(1)
        current_mode = mode_lookup.get(mode_code, 'UNKNOWN')

    # laser power
    power_match = power_pattern.search(line)
    if power_match:
        current_power = float(power_match.group(1))

    # feedrate
    feed_match = feed_pattern.search(line)
    if feed_match:
        current_feedrate = float(feed_match.group(1))

    # coordinates
    xyz_match = xyz_pattern.search(line)

    if xyz_match:

        x = float(xyz_match.group(1))
        y = float(xyz_match.group(2))
        z = float(xyz_match.group(3))

        laser_on = 'Q1=IC(72)' in line

        records.append({
            'line_number': line_number,
            'layer': current_layer,
            'mode': current_mode,
            'x': x,
            'y': y,
            'z': z,
            'feedrate_ipm': current_feedrate,
            'laser_power_w': current_power,
            'laser_on': laser_on,
            'raw_line': line
        })

#%%
# DATAFRAME

points_df = pd.DataFrame(records)

print(points_df.head())

print(f"\nExtracted {len(points_df)} motion points")

#%%
# BUILD VECTORS

vector_records = []

for i in range(1, len(points_df)):

    prev_row = points_df.iloc[i - 1]
    row = points_df.iloc[i]

    vector_records.append({
        'layer': row['layer'],
        'mode': row['mode'],

        'x1': prev_row['x'],
        'y1': prev_row['y'],
        'z1': prev_row['z'],

        'x2': row['x'],
        'y2': row['y'],
        'z2': row['z'],

        'feedrate_ipm': row['feedrate_ipm'],
        'laser_power_w': row['laser_power_w'],
        'laser_on': row['laser_on'],

        'line_number': row['line_number']
    })

vectors_df = pd.DataFrame(vector_records)


#%%
# -------------------------------------------------------------------
# GEOMETRIC METRICS


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

#%%
# -------------------------------------------------------------------
# TURN ANGLE
# -------------------------------------------------------------------

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

#%%
# -------------------------------------------------------------------
# TIME ESTIMATION
# -------------------------------------------------------------------

# convert inches/minute to inches/sec
vectors_df['feedrate_ips'] = vectors_df['feedrate_ipm'] / 60.0

vectors_df['travel_time_sec'] = (
    vectors_df['length'] /
    vectors_df['feedrate_ips']
)

vectors_df['start_time_sec'] = vectors_df['travel_time_sec'].cumsum().shift(fill_value=0)

vectors_df['end_time_sec'] = vectors_df['start_time_sec'] + vectors_df['travel_time_sec']

#%%
# -------------------------------------------------------------------
# VECTOR MIDPOINTS
# -------------------------------------------------------------------

vectors_df['xm'] = (vectors_df['x1'] + vectors_df['x2']) / 2
vectors_df['ym'] = (vectors_df['y1'] + vectors_df['y2']) / 2
vectors_df['zm'] = (vectors_df['z1'] + vectors_df['z2']) / 2

#%%
# -------------------------------------------------------------------
# THERMAL REVISIT METRIC
# -------------------------------------------------------------------

midpoints = vectors_df[['xm', 'ym']].values

kdtree = cKDTree(midpoints)

thermal_revisit = []

for i in range(len(vectors_df)):

    current_point = midpoints[i]

    neighbors = kdtree.query_ball_point(current_point, r=thermal_radius)

    current_start_time = vectors_df.iloc[i]['start_time_sec']

    previous_neighbors = [
        n for n in neighbors
        if n < i
    ]

    if len(previous_neighbors) == 0:
        thermal_revisit.append(np.nan)
        continue

    previous_times = vectors_df.iloc[previous_neighbors]['end_time_sec']

    delta_t = current_start_time - previous_times.max()

    thermal_revisit.append(delta_t)

vectors_df['thermal_revisit_sec'] = thermal_revisit

#%%
# -------------------------------------------------------------------
# ENERGY METRIC
# -------------------------------------------------------------------

vectors_df['linear_energy_density'] = (
    vectors_df['laser_power_w'] /
    vectors_df['feedrate_ips']
)

#%%
# -------------------------------------------------------------------
# VISUALIZATION 1
# RAW SCAN VECTORS
# -------------------------------------------------------------------

fig, ax = plt.subplots(figsize=(10, 10))

for _, row in vectors_df.iterrows():

    ax.arrow(
        row['x1'],
        row['y1'],
        row['dx'],
        row['dy'],
        head_width=0.02,
        length_includes_head=True,
        alpha=0.7
    )

ax.set_title('Raw Scan Vectors')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_aspect('equal')

plt.show()

#%%
# -------------------------------------------------------------------
# VISUALIZATION 2
# SEQUENTIAL COLORING
# -------------------------------------------------------------------

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

ax.set_title('Sequential Toolpath Execution')

plt.show()



#%%
# -------------------------------------------------------------------
# VISUALIZATION 3
# CONTOUR VS HATCH
# -------------------------------------------------------------------

fig, ax = plt.subplots(figsize=(10, 10))

mode_colors = {
    'CONTOUR': 'red',
    'HATCH': 'blue',
    'OTHER': 'gray'
}

for _, row in vectors_df.iterrows():

    ax.plot(
        [row['x1'], row['x2']],
        [row['y1'], row['y2']],
        color=mode_colors.get(row['mode'], 'black'),
        linewidth=2
    )

ax.set_title('Contour vs Hatch')
ax.set_aspect('equal')

plt.show()

#%%
# -------------------------------------------------------------------
# VISUALIZATION 4
# THERMAL REVISIT MAP
# -------------------------------------------------------------------

fig, ax = plt.subplots(figsize=(10, 10))

scatter = ax.scatter(
    vectors_df['xm'],
    vectors_df['ym'],
    c=vectors_df['thermal_revisit_sec'],
    s=25
)

plt.colorbar(scatter, label='Thermal Revisit Time (sec)')

ax.set_title('Thermal Revisit Map')
ax.set_aspect('equal')

plt.show()

#%%
# -------------------------------------------------------------------
# LAYER REPLAY ANIMATION
# -------------------------------------------------------------------

fig, ax = plt.subplots(figsize=(10, 10))

ax.set_xlim(vectors_df[['x1', 'x2']].min().min() - 0.1,
            vectors_df[['x1', 'x2']].max().max() + 0.1)

ax.set_ylim(vectors_df[['y1', 'y2']].min().min() - 0.1,
            vectors_df[['y1', 'y2']].max().max() + 0.1)

ax.set_aspect('equal')


def animate(i):

    ax.clear()

    subset = vectors_df.iloc[:i]

    for _, row in subset.iterrows():

        ax.plot(
            [row['x1'], row['x2']],
            [row['y1'], row['y2']],
            color='blue' if row['laser_on'] else 'gray'
        )

    ax.set_title(f'Toolpath Replay: Step {i}')
    ax.set_aspect('equal')


ani = FuncAnimation(
    fig,
    animate,
    frames=len(vectors_df),
    interval=0.5
)

plt.show()

#%%
# -------------------------------------------------------------------
# EXPORT
# -------------------------------------------------------------------

vectors_df.to_csv('rpmi_vectors.csv', index=False)

print('\nSaved vector dataset: rpmi_vectors.csv')

#%%
# -------------------------------------------------------------------
# SUMMARY STATISTICS
# -------------------------------------------------------------------

print('\n--- SUMMARY ---')

print(f'Total vectors: {len(vectors_df)}')
print(f'Total deposition distance: {vectors_df["length"].sum():.2f} inches')
print(f'Total build time estimate: {vectors_df["travel_time_sec"].sum()/60:.2f} minutes')
print(f'Mean vector length: {vectors_df["length"].mean():.3f} inches')
print(f'Mean thermal revisit: {vectors_df["thermal_revisit_sec"].mean():.2f} sec')

'''

# What This Pipeline Gives You

This creates:

* normalized process vectors
* manufacturing replay
* scan strategy visualization
* contour vs hatch separation
* thermal revisit metrics
* estimated timestamps
* geometric metrics
* energy metrics

# Immediate Thesis Extensions

## Add Thermocouple Synchronization

Map:

```text
vector timestamp
↔
TC timestamp
```

Then compute:

* peak temperature per vector
* local cooling rate
* reheating frequency

---

## Add Meltpool Monitoring

Map:

```text
vector
↔
camera frame
```

Then compute:

* meltpool width
* brightness
* instability
* spatter

---

## Compare RPMI vs Mazak

Compute differences in:

* hatch ordering
* contour sequencing
* thermal revisit
* path continuity
* corner behavior
* dead move overhead
* scan efficiency

---

## Build Knowledge Graph

Each vector becomes:

```text
(:Vector)
 ├── HAS_TIME
 ├── HAS_POSITION
 ├── USES_POWER
 ├── HAS_MODE
 ├── HAS_TEMPERATURE
 ├── HAS_MELTPOOL
 └── CONTRIBUTES_TO_DEFECT
```
'''



from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection='3d')

for _, row in vectors_df.iterrows():

    ax.plot(
        [row['x1'], row['x2']],
        [row['y1'], row['y2']],
        [row['z1'], row['z2']],
        alpha=0.7
    )

ax.set_title("3D Raw Scan Vectors")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")

plt.show()


import numpy as np
from mpl_toolkits.mplot3d.art3d import Line3DCollection

fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection='3d')

segments = []

for _, row in vectors_df.iterrows():
    segments.append([
        [row['x1'], row['y1'], row['z1']],
        [row['x2'], row['y2'], row['z2']]
    ])

lc = Line3DCollection(
    segments,
    cmap='viridis',
    linewidths=2
)

lc.set_array(np.arange(len(segments)))

ax.add_collection3d(lc)

ax.set_title("3D Sequential Toolpath Execution")

ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")

plt.colorbar(lc, label="Execution Order")

plt.show()

from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection='3d')

mode_colors = {
    'CONTOUR': 'red',
    'HATCH': 'blue',
    'OTHER': 'gray'
}

for _, row in vectors_df.iterrows():

    ax.plot(
        [row['x1'], row['x2']],
        [row['y1'], row['y2']],
        [row['z1'], row['z2']],
        color=mode_colors.get(row['mode'], 'black'),
        linewidth=2
    )

ax.set_title("3D Contour vs Hatch")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")

plt.show()

print("\nGeometry Extents")

print("X:",
      vectors_df[['x1','x2']].min().min(),
      "→",
      vectors_df[['x1','x2']].max().max())

print("Y:",
      vectors_df[['y1','y2']].min().min(),
      "→",
      vectors_df[['y1','y2']].max().max())

print("Z:",
      vectors_df[['z1','z2']].min().min(),
      "→",
      vectors_df[['z1','z2']].max().max())