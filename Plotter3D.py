import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.tri import Triangulation

def plot_double_integral(f, in_region, xlim, ylim, resolution=200):
    x = np.linspace(xlim[0], xlim[1], resolution)
    y = np.linspace(ylim[0], ylim[1], resolution)
    xv, yv = np.meshgrid(x, y)
    xv_flat = xv.flatten()
    yv_flat = yv.flatten()

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

    ax.plot_trisurf(tri, z_in, cmap=cm.viridis, edgecolor='none', alpha=0.9)
    ax.plot_trisurf(tri, np.zeros_like(z_in), color='lightgray', alpha=0.25)

    for i in range(len(z_in)):
        ax.plot([x_in[i], x_in[i]], [y_in[i], y_in[i]], [0, z_in[i]], color='gray', alpha=0.2)

    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.set_title("Double Integral Surface with Shaded Volume")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    import math

    print("Enter the function f(x, y) (use numpy functions, e.g., sin(x)*cos(y)):")
    func_str = input("f(x, y) = ")

    print("\nDefine the region R by a condition on x and y (e.g., x**2 + y**2 <= 4):")
    region_str = input("Region condition: ")

    print("\nEnter x bounds (e.g., -3, 3):")
    x_min, x_max = map(float, input("x_min, x_max = ").split(','))

    print("Enter y bounds (e.g., -3, 3):")
    y_min, y_max = map(float, input("y_min, y_max = ").split(','))

    # Allow numpy and math functions in eval context
    allowed_names = {
        k: v for k, v in vars(np).items() if not k.startswith("__")
    }
    allowed_names.update({'math': math, 'np': np})

    def f(x, y):
        return eval(func_str, allowed_names | {'x': x, 'y': y})

    def in_region(x, y):
        return eval(region_str, allowed_names | {'x': x, 'y': y})

    plot_double_integral(f, in_region, xlim=(x_min, x_max), ylim=(y_min, y_max))
