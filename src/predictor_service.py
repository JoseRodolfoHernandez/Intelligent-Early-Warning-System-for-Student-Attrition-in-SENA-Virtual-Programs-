import os
import pandas as pd
import joblib

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_assets():
    """Loads the real trained machine learning model and its core engineering columns"""
    model_path = os.path.join(BASE_DIR, 'attrition_model.pkl')
    columns_path = os.path.join(BASE_DIR, 'model_columns.pkl')
    return joblib.load(model_path), joblib.load(columns_path)

def make_prediction(data):
    """
    Receives data from the Flask HTML form, processes it through the 
    Data Engineering pipeline, and returns real ML model predictions.
    """
    try:
        # 1. Load the serialized ML assets
        model, model_columns = load_assets()

        # 2. Extract and cast inputs from the Flask HTML Form dictionary
        input_dict = {
            'NOMBRE_REGIONAL': f"REGIONAL {data.get('NOMBRE_REGIONAL', '').upper()}",
            'NIVEL_FORMACION': data.get('NIVEL_FORMACION', '').upper(),
            'TOTAL_APRENDICES_MATRICULADOS': int(data.get('TOTAL_APRENDICES_MATRICULADOS', 0)),
            'DURATION_DAYS': int(data.get('DURATION_DAYS', 0))
        }
        
        # 3. Data Engineering Transformation Pipeline (Match alignment matrix)
        input_df = pd.get_dummies(pd.DataFrame([input_dict]))
        
        # Reindex sparse matrix to match model training structures
        for col in model_columns:
            if col not in input_df.columns:
                input_df[col] = 0
        input_df = input_df[model_columns]
        
        # 4. Run Model Inference
        # If your model returns a probability score directly
        prediction_value = model.predict(input_df)[0]
        
        # Convert score to percentage format (Handle classification bounds)
        # Note: If predict() returns a class (0 or 1), use predict_proba(input_df)[0][1] instead.
        probability = float(prediction_value)
        if probability <= 1.0:
            probability = probability * 100  # Convert 0.23 to 23.0%
            
        # 5. UI Mapping Logic for Flask Rendering
        if probability >= 20.0:
            classification = "HIGH RISK"
            status_color = "danger"  # Bootstrap red alert
        elif probability >= 10.0:
            classification = "MEDIUM RISK"
            status_color = "warning" # Bootstrap orange alert
        else:
            classification = "LOW RISK"
            status_color = "success" # Bootstrap green alert
            
        return {
            "probability": round(probability, 2),
            "classification": classification,
            "status_color": status_color
        }

    except Exception as e:
        return {"error": f"Inference engine failure: {str(e)}"}