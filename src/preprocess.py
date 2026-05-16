import pandas as pd
import numpy as np

def clean_sena_data(input_path, output_path):
    print(f"--- Loading data from {input_path} ---")
    
    # We load the original file
    df = pd.read_csv(input_path, low_memory=False)
    
    # We remove double quotes (") that appear inside the text literally
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].str.replace('"', '', regex=False).str.strip()
    
    # 1. Filter by VIRTUAL modality (Now it will match)
    df_virtual = df[df['MODALIDAD_FORMACION'] == 'VIRTUAL'].copy()
    
    if df_virtual.empty:
        print("ALERTA: Sigue sin encontrar registros. Valores actuales en la columna:")
        print(df['MODALIDAD_FORMACION'].unique())
        return

    # 2. Convert dates
    df_virtual['FECHA_INICIO_FICHA'] = pd.to_datetime(df_virtual['FECHA_INICIO_FICHA'], format='%d/%m/%Y', errors='coerce')
    df_virtual['FECHA_TERMINACION_FICHA'] = pd.to_datetime(df_virtual['FECHA_TERMINACION_FICHA'], format='%d/%m/%Y', errors='coerce')
    
    # Calculate duration in days
    df_virtual['DURATION_DAYS'] = (df_virtual['FECHA_TERMINACION_FICHA'] - df_virtual['FECHA_INICIO_FICHA']).dt.days
    
    # 3. Calculate the Dropout Rate
    df_virtual['DESERTORES_AÑO_ACTUAL'] = pd.to_numeric(df_virtual['DESERTORES_AÑO_ACTUAL'], errors='coerce').fillna(0)
    df_virtual['TOTAL_APRENDICES_MATRICULADOS'] = pd.to_numeric(df_virtual['TOTAL_APRENDICES_MATRICULADOS'], errors='coerce').fillna(1)
    
    df_virtual['ATTRITION_RATE'] = df_virtual['DESERTORES_AÑO_ACTUAL'] / df_virtual['TOTAL_APRENDICES_MATRICULADOS']
    df_virtual['ATTRITION_RATE'] = df_virtual['ATTRITION_RATE'].replace([np.inf, -np.inf], 0).fillna(0)
    
   # 4. Select final columns
    features = [
        'NOMBRE_REGIONAL',
        'NIVEL_FORMACION',
        'TOTAL_APRENDICES_MATRICULADOS',
        'DURATION_DAYS',
        'ATTRITION_RATE'
    ]
    
    # We remove rows where the duration is negative or zero (date errors in source)
    df_final = df_virtual[df_virtual['DURATION_DAYS'] > 0][features].dropna()
    
    # Save the result
    df_final.to_csv(output_path, index=False)
    print(f"--- SUCCESS: Processed {len(df_final)} virtual records. ---")
    print(f"--- Saved to {output_path} ---")

if __name__ == "__main__":
    clean_sena_data('data/DESERCION_DE_LA_FORMACIÓN_PROFESIONAL_INTEGRAL_20260514.csv', 
                    'data/sena_virtual_cleaned.csv')