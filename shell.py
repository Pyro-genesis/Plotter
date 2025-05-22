import subprocess
import sys
import os

def run_script(script_name):
    if os.path.exists(script_name):
        subprocess.run([sys.executable, script_name])
    else:
        print(f"❌ Script '{script_name}' not found in the current directory.")

def main():
    print("=== Integral Plotter Launcher ===")
    print("Choose which type of integral to plot:")
    print("1. Single Variable (2D)")
    print("2. Double Variable (3D)")
    choice = input("Enter 1 or 2: ").strip()

    if choice == '1':
        run_script("Plotter2D.py")
    elif choice == '2':
        run_script("Plotter3D.py")
    else:
        print("⚠️ Invalid input. Please run the program again and enter 1 or 2.")

if __name__ == "__main__":
    main()