from flask import Flask, render_template, url_for
import os

app = Flask(__name__)

@app.route("/")
def index():
    # Define the path to the static folder.
    static_path = os.path.join(app.root_path, 'static')

    # List only CSV files.
    csv_files = [f for f in os.listdir(static_path) if f.endswith('.csv')]

    # Build a list of dictionaries containing file names and their URL paths.
    file_list = [{"name": f, "url": url_for('static', filename=f)} for f in csv_files]

    return render_template("home.html", csv_files=file_list)


if __name__ == "__main__":
    app.run(debug=True)
