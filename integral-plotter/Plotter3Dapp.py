import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.tri import Triangulation
import os
from datetime import datetime
import re
from app import func_str, X_BOUNDS, Y_BOUNDS, region_str

def sanitize_filename(name):
    return re.sub(r'[^a-zA-Z0-9_\-]', '_', name)

def read_resolution_from_settings(path="integral-plotter/settings.txt", default=80):
    try:
        with open(path, 'r') as file:
            for line in file:
                if "resolution3d:" in line:
                    start = line.find('{') + 1
                    end = line.find('}')
                    return int(line[start:end])
    except Exception as e:
        print(f"⚠️ Could not read resolution from integral-plotter/settings.txt: {e}")
    return default
def read_colormap_from_settings(path="integral-plotter/settings.txt", default="viridis"):
    try:
        with open(path, 'r') as file:
            for line in file:
                if "colormap:" in line:
                    start = line.find('{') + 1
                    end = line.find('}')
                    return line[start:end].strip()
    except Exception as e:
        print(f"⚠️ Could not read colormap from integral-plotter/settings.txt: {e}")
    return default

def plot_double_integral(f, in_region, xlim, ylim, resolution=read_resolution_from_settings()):
    x = np.linspace(xlim[0], xlim[1], resolution)
    y = np.linspace(ylim[0], ylim[1], resolution)
    xv, yv = np.meshgrid(x, y)
    xv_flat = xv.flatten()
    yv_flat = yv.flatten()
    cmap_name = read_colormap_from_settings()

    points = np.array([
        (x, y) for x, y in zip(xv_flat, yv_flat) if in_region(x, y)
    ])
    if len(points) == 0:
        raise ValueError("No points found in the region R.")
   
    x_in = points[:, 0]
    y_in = points[:, 1]
    z_in = f(x_in, y_in)

    tri = Triangulation(x_in, y_in)

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    ax.plot_trisurf(tri, z_in, cmap=plt.colormaps[cmap_name], edgecolor='none', alpha=0.9)
    ax.plot_trisurf(tri, np.zeros_like(z_in), color='lightgray', alpha=0.25)

    for i in range(len(z_in)):
        ax.plot([x_in[i], x_in[i]], [y_in[i], y_in[i]], [0, z_in[i]], color='gray', alpha=0.2)

    ax.plot_trisurf(x_in, y_in, np.zeros_like(z_in), color='lightgrey', alpha=0.3)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.set_title("Double Integral Surface Render with Shaded Volume: " + entryType + ' within ' + entryTypeRegion)
    plt.show()
    plt.tight_layout()
    func_name = sanitize_filename(func_str.split('(')[0].strip())  # crude extraction before "(" if any
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    folder = "functions"
    os.makedirs(folder, exist_ok=True)
    filename = f"2I_{func_name}-{timestamp}.png"
    filepath = os.path.join(folder, filename)
    plt.tight_layout()
    plt.savefig(filepath)
    print(f"✅ Plot saved as {filepath}; Please download it from the functions folder.")


if __name__ == "__main__":
    import math

    # Replace ln(x) with log(x) to support natural log with 'ln' notation
    entryType = func_str
    entryType = entryType.replace("**", "^")
    entryType = entryType.replace("log(", "ln(")
    func_str = func_str.replace("ln(", "log(")
    func_str = func_str.replace("^", "**")  # Replace ^ with ** for power operator

    # Replace ln(x) with log(x) to support natural log with 'ln' notation
    entryTypeRegion = region_str
    entryTypeRegion = entryTypeRegion.replace("**", "^")
    entryTypeRegion = entryTypeRegion.replace("log(", "ln(")
    region_str = region_str.replace("ln(", "log(")
    region_str = region_str.replace("^", "**")  # Replace ^ with ** for power operator

    x_min, x_max = map(float, X_BOUNDS.split(','))

    print("Enter y bounds (e.g., -3, 3):")
    y_min, y_max = map(float, Y_BOUNDS.split(','))

    # Allow numpy and math functions in eval context
    allowed_names = {
        k: v for k, v in vars(np).items() if not k.startswith("__")
    }
    allowed_names.update({'math': math, 'np': np})

    def f(x, y):
        return eval(func_str, allowed_names | {'x': x, 'y': y})

    if region_str.strip() == "":
        def in_region(x, y):
            return True
    else:
        def in_region(x, y):
            try:
                return eval(region_str, allowed_names | {'x': x, 'y': y})
            except:
                return False

    
    plot_double_integral(f, in_region, xlim=(x_min, x_max), ylim=(y_min, y_max))