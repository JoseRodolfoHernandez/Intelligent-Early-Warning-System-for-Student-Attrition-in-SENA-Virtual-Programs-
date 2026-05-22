from flask import Flask, render_template, request
import os
from predictor_service import make_prediction

src_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(src_dir)
templates_dir = os.path.join(project_root, 'templates')

app = Flask(__name__, template_folder=templates_dir)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/business-understanding')
def business_understanding():
    return render_template('business.html')

@app.route('/data-understanding')
def data_understanding():
    return render_template('understanding.html')

@app.route('/data-engineering')
def data_engineering():
    return render_template('engineering.html')

# NEW MENU: Model Engineering
@app.route('/model-engineering')
def model_engineering():
    return render_template('modeling.html')

# NEW MENU: Model Evaluation
@app.route('/model-evaluation')
def model_evaluation():
    return render_template('evaluation.html')

# CRITICAL NEW MENU: Prediction System (Handles GET and POST)
@app.route('/prediction-system', methods=['GET', 'POST'])
def prediction_system():
    result = None
    form_data = {}
    if request.method == 'POST':
        try:
            form_data = {
                'NOMBRE_REGIONAL': request.form.get('regional'),
                'NIVEL_FORMACION': request.form.get('nivel'),
                'TOTAL_APRENDICES_MATRICULADOS': request.form.get('matriculados'),
                'DURATION_DAYS': request.form.get('duration')
            }
            # Execute backend prediction logic
            result = make_prediction(form_data)
        except Exception as e:
            result = {"error": f"Form parsing failure: {str(e)}"}
            
    return render_template('prediction.html', result=result, form=form_data)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)