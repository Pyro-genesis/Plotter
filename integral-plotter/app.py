import os
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Folder where example and generated images are stored
IMAGE_FOLDER = "static/functions"
EXAMPLE_IMAGE = "doubled_integral_plot_example.png"

@app.route("/", methods=["GET", "POST"])
def index():
    plot_image = EXAMPLE_IMAGE  # default image to show

    if request.method == "POST":
        integral_type = request.form.get("integral_type")
        func_str = request.form.get("function")
        region_str = request.form.get("region", "")
        x_bounds = request.form.get("x_bounds")
        y_bounds = request.form.get("y_bounds", "")

        # Validate required fields simply
        if not function or not x_bounds:
            return render_template("index.html", error="Please fill in required fields.", 
                                   integral_type=integral_type, plot_image=plot_image)

        # Save inputs as environment variables for subprocess
        env = os.environ.copy()
        env["FUNCTION"] = func_str
        env["X_BOUND"] = x_bounds
        env["Y_BOUND"] = y_bounds if integral_type == "double" else ""
        env["REGION"] = region_str if integral_type == "double" else ""

        # Choose script to run
        script = "Plotter3Dapp.py" if integral_type == "double" else "Plotter2Dapp.py"

        # Run the plotting script
        import subprocess
        try:
            subprocess.run([sys.executable, script], env=env, check=True)
        except subprocess.CalledProcessError:
            return render_template("index.html", error="Failed to generate plot.", 
                                   integral_type=integral_type, plot_image=plot_image)

        # After successful plot generation, find the newest plot image file (you save with timestamp in plotter)
        # Assume files saved to functions, pick latest .png file
        files = [f for f in os.listdir(functions) if f.endswith(".png")]
        if files:
            latest_file = max(files, key=lambda f: os.path.getctime(os.path.join(IMAGE_FOLDER, f)))
            plot_image = latest_file

        return render_template("index.html", integral_type=integral_type, plot_image=plot_image)

    # GET request: show default page with example image and no errors
    return render_template("index.html", integral_type="single", plot_image=plot_image)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
