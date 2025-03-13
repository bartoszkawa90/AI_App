from flask import Flask, render_template, url_for, jsonify, request
import os

app = Flask(__name__)

@app.route('/')
def index():
    # Define the path to the 'stocks' folder within the static directory
    stocks_path = os.path.join(app.root_path, 'static', 'stocks')

    # List only CSV files in the stocks directory
    csv_files = [f.split('.')[0] for f in os.listdir(stocks_path) if f.endswith('.csv')]

    # Build a list of dictionaries containing file names and their URL paths
    file_list = [
        {"name": f, "url": url_for('static', filename=f'stocks/{f}.csv')}
        for f in csv_files
    ]

    return render_template("home.html", csv_files=file_list)

@app.route('/update', methods=['POST'])
def update():
    pass

if __name__ == '__main__':
    app.run(debug=True)
