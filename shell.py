import subprocess
import sys
import os
import re
import matplotlib.pyplot as plt

SETTINGS_FILE = "settings.txt"

def run_script(script_name):
    if os.path.exists(script_name):
        subprocess.run([sys.executable, script_name])
    else:
        print(f"❌ Script '{script_name}' not found in the current directory.")

def update_setting(key, value):
    updated = False
    lines = []
    
    # Format: key {value}
    new_line = f"{key} {{{value}}}\n"
    
    # Read or create settings
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r') as file:
            for line in file:
                if line.strip().startswith(key):
                    lines.append(new_line)
                    updated = True
                else:
                    lines.append(line)
    if not updated:
        lines.append(new_line)
    
    # Write back
    with open(SETTINGS_FILE, 'w') as file:
        file.writelines(lines)
    
    print(f"✅ Updated setting: {key[:-1]} = {value}")

def handle_command(command):
    parts = command.strip().split()
    if len(parts) < 3:
        print("⚠️ Invalid settings command. Usage: /settings res2d 100 or /settings cm viridis")
        return
    
    _, key, value = parts[0], parts[1], ' '.join(parts[2:])
    
    if key.lower() in ["resolution2d", "res2d"]:
        if not value.isdigit():
            print("⚠️ Resolution must be a number.")
            return
        update_setting("resolution2d:", value)
    elif key.lower() in ["cm", "colormap"]:
        if value not in plt.colormaps():
            print("⚠️ Invalid colormap name.")
            return
        else:
            update_setting("colormap:", value)
    elif key.lower() in ["resolution3d", "res3d"]:
        if not value.isdigit():
            print("⚠️ Resolution must be a number.")
            return
        else:
            update_setting("resolution3d:", value)
    else:
        print("⚠️ Unknown setting key.")

def main():
    print("=== Integral Plotter Shell ===")
    print("Type `/settings resolution <integer>` or `/settings cm <colormap>` to update settings.")
    print("Or choose a plotter:")
    print("1. Single Integral (2D)")
    print("2. Double Integral (3D)")

    user_input = input("Input: ").strip()

    if user_input.startswith("/settings"):
        handle_command(user_input)
    elif user_input == '1':
        run_script("Plotter2D.py")
    elif user_input == '2':
        run_script("Plotter3D.py")
    else:
        print("⚠️ Invalid input.")

if __name__ == "__main__":
    main()
# This script is a launcher for the integral plotter scripts.
# It allows the user to set parameters and choose between 2D and 3D plotting.
# The settings are stored in a file called settings.txt.