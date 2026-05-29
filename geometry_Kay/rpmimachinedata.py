#%%
# =========================================================
# LOAD TELEMETRY DATA
# =========================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from mpl_toolkits.mplot3d import Axes3D
from scipy.spatial import ConvexHull


# ---------------------------------------------------------
# FILE PATH
# ---------------------------------------------------------

data_path = r"C:\Users\Kayleigh\DIGITAL_ARCH_REPO\build_telemetry.csv"

# Load CSV
data = pd.read_csv(data_path)

print("\nLoaded Data:")
print(data.head())

print("\nColumns:")
print(data.columns.tolist())


# =========================================================
# POSITION COLUMN NAMES
# =========================================================
# CHANGE THESE TO MATCH YOUR CSV

TIME_COLUMN = "TimeStamp"   # <-- CHANGE THIS
X_COL = "Pos X(inch)"                 # <-- CHANGE THIS
Y_COL = "Pos Y(inch)"                 # <-- CHANGE THIS
Z_COL = "Pos Z(inch)"                 # <-- CHANGE THIS

# Keep only XYZ

xyz_data = data[[X_COL, Y_COL, Z_COL]].copy()

# Remove NaN rows
xyz_data = xyz_data.dropna()

print("\nXYZ DATA:")
print(xyz_data.head())


# =========================================================
# FUNCTION:
# CREATE SYNTHETIC HIGH FREQUENCY DATA
# =========================================================
#
# Example:
# 1 Hz original points:
#
# P1 -------- P2
#
# Create random interpolated points between them
#
# 10 Hz:
# create 9 new points between each original point
#
# 100 Hz:
# create 99 new points between each original point
#
# Adds slight random noise to simulate telemetry variation
#
# =========================================================

def generate_high_frequency_data(
    df,
    multiplier=10,
    noise_scale=0.01
):

    synthetic_points = []

    for i in range(len(df) - 1):

        # Current point
        p1 = df.iloc[i].values

        # Next point
        p2 = df.iloc[i + 1].values

        # Add original point
        synthetic_points.append(p1)

        # Create interpolated points
        for j in range(1, multiplier):

            # Interpolation fraction
            t = j / multiplier

            # Linear interpolation
            interp = p1 + (p2 - p1) * t

            # Add random noise
            noise = np.random.normal(
                0,
                noise_scale,
                size=3
            )

            interp = interp + noise

            synthetic_points.append(interp)

    # Add final point
    synthetic_points.append(df.iloc[-1].values)

    # Convert back to dataframe
    synthetic_df = pd.DataFrame(
        synthetic_points,
        columns=[X_COL, Y_COL, Z_COL]
    )

    return synthetic_df


# =========================================================
# CREATE 10 Hz DATA
# =========================================================

data_10hz = generate_high_frequency_data(
    xyz_data,
    multiplier=10,
    noise_scale=0.01
)

print("\n10 Hz Data Shape:")
print(data_10hz.shape)


# =========================================================
# CREATE 100 Hz DATA
# =========================================================

data_100hz = generate_high_frequency_data(
    xyz_data,
    multiplier=100,
    noise_scale=0.005
)

print("\n100 Hz Data Shape:")
print(data_100hz.shape)


# =========================================================
# SAVE GENERATED DATA
# =========================================================

data_10hz.to_csv(
    r"C:\Users\Kayleigh\DIGITAL_ARCH_REPO\build_telemetry_10hz.csv",
    index=False
)

data_100hz.to_csv(
    r"C:\Users\Kayleigh\DIGITAL_ARCH_REPO\build_telemetry_100hz.csv",
    index=False
)

print("\nSaved synthetic datasets.")



# =========================================================
# 3D PLOT FUNCTION
# =========================================================
scale_factor = 2.0 / 1.338
def plot_3d(df, title):

    fig = plt.figure(figsize=(10, 8))

    ax = fig.add_subplot(111, projection='3d')

    # Color by point order
    colors = np.arange(len(df))

    scatter = ax.scatter(
        df[X_COL]*scale_factor,
        df[Y_COL]*scale_factor,
        df[Z_COL]*scale_factor,
        c=colors,
        s=1
    )

    # Optional trajectory line
    ax.plot(
        df[X_COL]*scale_factor,
        df[Y_COL]*scale_factor,
        df[Z_COL]*scale_factor,
        linewidth=0.3
    )

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

    ax.set_title(title)

    plt.tight_layout()
    plt.show()


# =========================================================
# PLOT ORIGINAL 1 Hz DATA
# =========================================================

plot_3d(
    xyz_data,
    "Original 1 Hz Position Data"
)


# =========================================================
# PLOT 10 Hz DATA
# =========================================================

plot_3d(
    data_10hz,
    "Synthetic 10 Hz Position Data"
)


# =========================================================
# PLOT 100 Hz DATA
# =========================================================

plot_3d(
    data_100hz,
    "Synthetic 100 Hz Position Data"
)




def plot_3d_contours(contours, title):

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    for z, contour in contours.items():

        xs = contour[:, 0]
        ys = contour[:, 1]
        zs = np.full_like(xs, z)

        ax.plot(xs, ys, zs, linewidth=1)

    ax.set_title(title)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

    plt.show()


# =========================================================
# LAYERED CONTOUR EXTRACTION (IMPORTANT FIX AREA)
# =========================================================

def get_layer_contours(df, z_step=0.015):  # <-- inches assumed

    df = df.copy()

    df["z_layer"] = (df[Z_COL]*scale_factor / z_step).round() * z_step

    contours = {}

    for z in sorted(df["z_layer"].unique()):

        layer = df[df["z_layer"] == z]

        pts = (layer[[X_COL, Y_COL]].values)*scale_factor

        if len(pts) < 4:
            continue

        try:
            hull = ConvexHull(pts)
            contour = pts[hull.vertices]
            contour = np.vstack([contour, contour[0]])

            contours[z] = contour

        except:
            continue

    return contours

# =========================================================
# CONVERT CONTOURS → VECTOR FORMAT (YOUR STYLE)
# =========================================================

def contours_to_vectors(contours):

    vectors = []

    for z, contour in contours.items():

        closed = np.vstack([contour, contour[0]])

        for i in range(len(closed) - 1):

            x1, y1 = closed[i]
            x2, y2 = closed[i + 1]

            vectors.append({
                "x1": x1,
                "y1": y1,
                "z1": z,
                "x2": x2,
                "y2": y2,
                "z2": z
            })

    return pd.DataFrame(vectors)

# =========================================================
# VECTOR PLOTTING
# =========================================================

def plot_vectors(df, title):

    fig = plt.figure(figsize=(10,10))
    ax = fig.add_subplot(111, projection='3d')

    for _, row in df.iterrows():

        ax.plot(
            [row['x1'], row['x2']],
            [row['y1'], row['y2']],
            [row['z1'], row['z2']],
            alpha=0.7
        )

    ax.set_title(title)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

    plt.show()

# =========================================================
# PIPELINE EXECUTION (CORRECT ORDER)
# =========================================================

contours_1hz = get_layer_contours(xyz_data, z_step=0.015)
contours_10hz = get_layer_contours(data_10hz, z_step=0.015)
contours_100hz = get_layer_contours(data_100hz, z_step=0.015)

vec_1hz = contours_to_vectors(contours_1hz)
vec_10hz = contours_to_vectors(contours_10hz)
vec_100hz = contours_to_vectors(contours_100hz)

plot_vectors(vec_1hz, "1 Hz Contour Vectors")
plot_vectors(vec_10hz, "10 Hz Contour Vectors")
plot_vectors(vec_100hz, "100 Hz Contour Vectors")




print("\nTelemetry Geometry Extents")

print("X:",
      xyz_data[X_COL].min(),
      "→",
      xyz_data[X_COL].max())

print("Y:",
      xyz_data[Y_COL].min(),
      "→",
      xyz_data[Y_COL].max())

print("Z:",
      xyz_data[Z_COL].min(),
      "→",
      xyz_data[Z_COL].max())

x_size = xyz_data[X_COL].max() - xyz_data[X_COL].min()
y_size = xyz_data[Y_COL].max() - xyz_data[Y_COL].min()
z_size = xyz_data[Z_COL].max() - xyz_data[Z_COL].min()

print("\nTelemetry Dimensions")
print("Width X:", x_size)
print("Depth Y:", y_size)
print("Height Z:", z_size)

