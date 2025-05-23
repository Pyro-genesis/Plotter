import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math
import os
from datetime import datetime
import re

# Safe eval context
math_context = {k: getattr(math, k) for k in dir(math) if not k.startswith("_")}
math_context.update({'np': np})

def change_formatting(expr):
    expr = expr.replace("ln(", "log(")
    expr = expr.replace("^", "**")  # Replace ^ with ** for power operator
    return expr

def read_resolution_from_settings(path="integral-plotter/settings.txt", default=500):
    try:
        with open(path, 'r') as file:
            for line in file:
                if "resolutionSurface:" in line:
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

def safe_eval(expr, **kwargs):
    local_context = {**math_context, **kwargs}
    return eval(expr, {"__builtins__": {}}, local_context)
def sanitize_filename(name):
    return re.sub(r'[^a-zA-Z0-9_\-]', '_', name)

def get_user_input():
    print("Enter parametric surface:")
    x_expr = input("x(u,v) = ")
    x_expr= change_formatting(x_expr)
    y_expr = input("y(u,v) = ")
    y_expr = change_formatting(y_expr)
    z_expr = input("z(u,v) = ")
    z_expr = change_formatting(z_expr)

    print("\nEnter scalar field f(x,y,z):")
    f_expr = input("f(x,y,z) = ")
    f_expr = change_formatting(f_expr)
    
    print("\nEnter bounds:")
    u_min = float(input("u_min = "))
    u_max = float(input("u_max = "))
    v_min = float(input("v_min = "))
    v_max = float(input("v_max = "))

    return x_expr, y_expr, z_expr, f_expr, u_min, u_max, v_min, v_max

def plot_surface(x_expr, y_expr, z_expr, f_expr, u_min, u_max, v_min, v_max):
    u = np.linspace(u_min, u_max, resolution)
    v = np.linspace(v_min, v_max, resolution)
    U, V = np.meshgrid(u, v)

    # Compute parametric surface
    X = safe_eval(x_expr, u=U, v=V)
    Y = safe_eval(y_expr, u=U, v=V)
    Z = safe_eval(z_expr, u=U, v=V)

    # Evaluate scalar field on surface
    F = safe_eval(f_expr, x=X, y=Y, z=Z)

    # Plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    surf = ax.plot_surface(X, Y, Z, facecolors=plt.colormaps[cmap_name](F / np.max(F)), rstride=1, cstride=1, linewidth=0, antialiased=False)

    ax.set_title("Surface colored by f(x, y, z)")
    plt.colorbar(surf, ax=ax, shrink=0.5, aspect=10, label='f(x, y, z)')
    plt.show()
    plt.tight_layout()
    func_name = sanitize_filename(f_expr.split('(')[0].strip())  # crude extraction before "(" if any
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    folder = "functions/Surface_Integrals"
    os.makedirs(folder, exist_ok=True)
    filename = f"SI_{func_name}-{timestamp}.png"
    filepath = os.path.join(folder, filename)
    plt.tight_layout()
    plt.savefig(filepath)
    print(f"✅ Plot saved as {filepath}; Please download it from the functions/surface_integrals folder.")


if __name__ == "__main__":
    resolution = read_resolution_from_settings()
    cmap_name = read_colormap_from_settings()
    x_expr, y_expr, z_expr, f_expr, u_min, u_max, v_min, v_max = get_user_input()
    plot_surface(x_expr, y_expr, z_expr, f_expr, u_min, u_max, v_min, v_max)