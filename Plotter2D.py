import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import os
from datetime import datetime
import re

def sanitize_filename(name):
    return re.sub(r'[^a-zA-Z0-9_\-]', '_', name)

def read_resolution_from_settings(path="settings.txt", default=500):
    try:
        with open(path, 'r') as file:
            for line in file:
                if "resolution" in line:
                    start = line.find('{') + 1
                    end = line.find('}')
                    return int(line[start:end])
    except Exception as e:
        print(f"⚠️ Could not read resolution from settings.txt: {e}")
    return default

def read_colormap_from_settings(path="settings.txt", default="viridis"):
    try:
        with open(path, 'r') as file:
            for line in file:
                if "colormap" in line:
                    start = line.find('{') + 1
                    end = line.find('}')
                    return line[start:end].strip()
    except Exception as e:
        print(f"⚠️ Could not read colormap from settings.txt: {e}")
    return default

def plot_single_integral(f, xlim, resolution=read_resolution_from_settings()):
    x = np.linspace(xlim[0], xlim[1], resolution)
    y = f(x)
    cmap_name = read_colormap_from_settings()

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(x, y, 'b', linewidth=2)
    ax.fill_between(x, 0, y, color=plt.colormaps[cmap_name](0.5), alpha=0.6)

    ax.axhline(0, color='gray', linewidth=0.8)
    ax.set_xlabel('x')
    ax.set_ylabel('f(x)')
    ax.set_title('Single Integral Area Render Under Curve: ' + func_str)
    ax.grid(True)

    plt.tight_layout()
    func_name = sanitize_filename(func_str.split('(')[0].strip())
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    folder = "functions"
    os.makedirs(folder, exist_ok=True)
    filename = f"1I_{func_name}-{timestamp}.png"
    filepath = os.path.join(folder, filename)
    plt.savefig(filepath)
    plt.show()
    print(f"✅ Plot saved as {filepath}")

if __name__ == "__main__":
    import math

    print("Enter the function f(x) (use numpy functions, e.g., sin(x) + x**2):")
    func_str = input("f(x) = ")
    # Replace ln(x) with log(x) to support natural log with 'ln' notation
    func_str = func_str.replace("ln(", "log(")
    func_str = func_str.replace("^", "**")


    print("\nEnter x bounds (e.g., 0, 5):")
    x_min, x_max = map(float, input("x_min, x_max = ").split(','))

    allowed_names = {k: v for k, v in vars(np).items() if not k.startswith("__")}
    allowed_names.update({'math': math, 'np': np})

    def f(x):
        return eval(func_str, allowed_names | {'x': x})

    plot_single_integral(f, xlim=(x_min, x_max))