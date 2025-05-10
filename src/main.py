"""Main entry point for Bookstore Management System"""

from flask import Flask, render_template
import pandas as pd

app = Flask(__name__, template_folder="../templates")

bookstore_db_path = "dataset/bookstore_db.csv"

# --- LOAD DATA ON STARTUP ---
# Read CSV into pandas DataFrame when app starts
inventory_df = pd.read_csv(bookstore_db_path)

# --- ROUTES ---
@app.route('/')
def home():
    return render_template('home.html', title="Group 2 Bookstore Management System")

# Placeholder routes for modularization
@app.route('/inventory')
def inventory():
    # Just show column names as a demo
    # Convert the dataframe to HTML for better display
    inventory_html = inventory_df.to_html(classes='table table-striped')
    return render_template('inventory.html', inventory=inventory_html)

@app.route('/customer_order')
def customer_order():
    return "Customer order module will go here."

@app.route('/supplier_order')
def supplier_order():
    return "Supplier order module will go here."

@app.route('/records')
def records():
    return "Records module will go here."
    

if __name__=="__main__":
    app.run(debug=True)