from flask import Flask, render_template
import os

src_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(src_dir)
templates_dir = os.path.join(project_root, 'templates')

app = Flask(__name__, template_folder=templates_dir)

# 1. Home
@app.route('/')
def home():
    return render_template('home.html')

# 2. CRISP-ML Methodology (¡El que nos faltaba!)
@app.route('/crisp-ml')
def crisp_ml():
    return render_template('crisp_ml.html')

# 3. Phase 1 - Business Understanding
@app.route('/business-understanding')
def business_understanding():
    return render_template('business.html')

# 4. Phase 2 - Data Understanding
@app.route('/data-understanding')
def data_understanding():
    return render_template('understanding.html')

# 5. Phase 3 - Data Engineering
@app.route('/data-engineering')
def data_engineering():
    return render_template('engineering.html')

if __name__ == '__main__':
    app.run(debug=True)