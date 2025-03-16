from flask import Flask, render_template, url_for, jsonify, request
import os
import glob
from list_of_actions import stocks
from data_operations import download_stock_data

app = Flask(__name__)
STOCKS_DIR = os.path.join(app.root_path, 'static', 'stocks')

@app.route('/')
def index():
    """Renders the home page with the list of available CSV files."""
    # collect names and paths to all csv file from static/stocks/ to be used for charts
    csv_files = [
        {"name": f.split('.')[0], "url": url_for('static', filename=f'stocks/{f}')}
        for f in os.listdir(STOCKS_DIR) if f.endswith('.csv')
    ]
    print(csv_files)
    return render_template("home.html", csv_files=csv_files)

@app.route('/update', methods=['POST'])
def update():
    """Deletes old stock CSV files and downloads new ones."""
    print("Updating stock data...")
    # remove all existing CSV files from static/stocks dir
    try:
        for file_path in glob.glob(os.path.join(STOCKS_DIR, '*.csv')):
            os.remove(file_path)
    except Exception as e:
        return jsonify({"message": "Error removing old files", "error": str(e)}), 500

    errors = []
    for idx, stock in enumerate(stocks[:5]):
        try:
            file_path = os.path.join(STOCKS_DIR, f"{idx}_{stock[1]}.csv")
            download_stock_data(stock[0], file_path, '3y', '1wk')
        except Exception as e:
            errors.append(f"Failed to download {stock[1]}: {str(e)}")

    if errors:
        return jsonify({"message": "Update completed with errors", "errors": errors}), 500
    return jsonify({"message": "Stock data updated successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)
