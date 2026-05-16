import pandas as pd
import joblib

def make_prediction(new_data_dict):
   # 1. Load the model and the saved columns
    model = joblib.load('src/attrition_model.pkl')
    model_columns = joblib.load('src/model_columns.pkl')
    
    # 2. Convert the new data to DataFrame
    input_df = pd.DataFrame([new_data_dict])
    
    # 3. Process Categories (One-Hot Encoding)
    input_df = pd.get_dummies(input_df)
    
    # 4. Align Columns (Ensure it has the same columns as the training)
    # If a column is missing, create it with a value of 0
    for col in model_columns:
        if col not in input_df.columns:
            input_df[col] = 0
    
    # Reorder columns so that they match exactly
    input_df = input_df[model_columns]
    
    # 5. Make the prediction
    prediction = model.predict(input_df)[0]
    return prediction

if __name__ == "__main__":
    # EXAMPLE: Data from a new Virtual Card
    nueva_ficha = {
        'NOMBRE_REGIONAL': 'REGIONAL ANTIOQUIA',
        'NIVEL_FORMACION': 'TECNOLOGO',
        'TOTAL_APRENDICES_MATRICULADOS': 50,
        'COURSE_DURATION_DAYS': 540 # Approximately 18 months
    }
    
    resultado = make_prediction(nueva_ficha)
    print(f"--- Predicción de Riesgo ---")
    print(f"Probabilidad estimada de deserción: {resultado:.2%}")