"""Main entry point for Bookstore Management System"""

from flask import Flask, render_template, request, redirect
import pandas as pd
import os

# Create Flask app and tell it where to find templates and static files
app = Flask(__name__, 
           template_folder="../templates",
           static_folder="../static")

# Get full path to the CSV database
bookstore_db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "dataset", "bookstore_db.csv"))

# Home page
@app.route('/')
def home():
    return render_template('home.html', title="Group 2 Bookstore Management System")

# Inventory display and logic
@app.route('/inventory')
def inventory():
    try:
        # Load inventory CSV
        df = pd.read_csv(bookstore_db_path)

        # Add necessary columns if they don't exist
        if 'Available_Count' not in df.columns:
            df['Available_Count'] = df['Quantity']
        if 'Reserved_Count' not in df.columns:
            df['Reserved_Count'] = 0
        if 'Checked_Out_Count' not in df.columns:
            df['Checked_Out_Count'] = 0
        if 'Lost_Count' in df.columns:
            df.drop(columns=['Lost_Count'], inplace=True)  # Remove deprecated Lost column

        # Stock status is based only on available books
        df['Stock'] = df['Available_Count'].apply(lambda x: 'Out of stock' if x == 0 else 'In stock')

        # Save updates
        df.to_csv(bookstore_db_path, index=False)

        # Send inventory to template
        return render_template('inventory.html', books=df.to_dict(orient='records'))
    except Exception as e:
        print(f"Error loading inventory: {str(e)}")
        return f"Error loading inventory: {str(e)}"

# Update inventory based on user input
@app.route('/update_status', methods=['POST'])
def update_status():
    try:
        title = request.form.get('title')  # Book title
        action = request.form.get('status')  # What the user selected (e.g., "Checked Out")
        quantity_change = request.form.get('quantity_change')  # Optional number input

        # Load current data
        df = pd.read_csv(bookstore_db_path)
        mask = df['Title'] == title  # Find the row for the given book

        # Make sure required columns exist
        for col in ['Available_Count', 'Reserved_Count', 'Checked_Out_Count']:
            if col not in df.columns:
                df[col] = 0

        # Convert quantity input to integer
        if quantity_change:
            try:
                quantity_change = int(quantity_change)
            except ValueError:
                quantity_change = 0
        else:
            quantity_change = 0

        # Logic for each action type
        if action == "Add Book" and quantity_change > 0:
            df.loc[mask, 'Quantity'] += quantity_change
            df.loc[mask, 'Available_Count'] += quantity_change
        elif action == "Checked Out" and quantity_change > 0:
            available = df.loc[mask, 'Available_Count'].values[0]
            if available >= quantity_change:
                df.loc[mask, 'Checked_Out_Count'] += quantity_change
                df.loc[mask, 'Available_Count'] -= quantity_change
        elif action == "Reserved" and quantity_change > 0:
            available = df.loc[mask, 'Available_Count'].values[0]
            if available >= quantity_change:
                df.loc[mask, 'Reserved_Count'] += quantity_change
                df.loc[mask, 'Available_Count'] -= quantity_change
        elif action == "Lost" and quantity_change > 0:
            available = df.loc[mask, 'Available_Count'].values[0]
            quantity = df.loc[mask, 'Quantity'].values[0]
            if quantity >= quantity_change:
                df.loc[mask, 'Quantity'] -= quantity_change
                if available >= quantity_change:
                    df.loc[mask, 'Available_Count'] -= quantity_change
        elif action == "Return" and quantity_change > 0:
            checked_out = df.loc[mask, 'Checked_Out_Count'].values[0]
            if checked_out >= quantity_change:
                df.loc[mask, 'Checked_Out_Count'] -= quantity_change
                df.loc[mask, 'Available_Count'] += quantity_change

        # Update stock display
        df['Stock'] = df['Available_Count'].apply(lambda x: 'Out of stock' if x == 0 else 'In stock')

        # Save updates
        df.to_csv(bookstore_db_path, index=False)
        return redirect('/inventory')
    except Exception as e:
        print(f"Error updating inventory: {str(e)}")
        return f"Error updating inventory: {str(e)}"

# Placeholder pages for future development
@app.route('/customer_order')
def customer_order():
    return "Customer order module will go here."

@app.route('/supplier_order')
def supplier_order():
    return "Supplier order module will go here."

@app.route('/records')
def records():
    return "Records module will go here."

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
# 