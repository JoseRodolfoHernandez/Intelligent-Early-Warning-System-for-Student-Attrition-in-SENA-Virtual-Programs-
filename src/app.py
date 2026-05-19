from flask import Flask, render_template
import os

app = Flask(__name__, template_folder='../templates')

# ROUTE 1: Home Menu
@app.route('/')
def home():
    return render_template('home.html')

# ROUTE 2: Phase 1 - Business Understanding
@app.route('/business-understanding')
def business_understanding():
    return render_template('business.html')

# ROUTE 3: Phase 2 - Data Understanding
@app.route('/data-understanding')
def data_understanding():
    return render_template('understanding.html')

# ROUTE 4: Phase 3 - Data Engineering
@app.route('/data-engineering')
def data_engineering():
    return render_template('engineering.html')

if __name__ == '__main__':
    app.run(debug=True)