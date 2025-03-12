from flask import Flask, render_template, url_for
import os
from data_operations import download_stock_data, get_stock_data_from_csv
from list_of_actions import stocks

app = Flask(__name__)

@app.route("/")
def index():
    # Define the path to the static folder.
    static_path = os.path.join(app.root_path, 'static')

    # List only CSV files.
    csv_files = [f.split('.')[0] for f in os.listdir(static_path) if f.endswith('.csv')]

    # Build a list of dictionaries containing file names and their URL paths.
    file_list = [{"name": f, "url": url_for('static', filename=f)} for f in csv_files]

    return render_template("home.html", csv_files=file_list)

@app.route('/update', methods=['POST'])
def update():
    """Collect new data from all considered stocks"""



if __name__ == "__main__":
    app.run(debug=True)
