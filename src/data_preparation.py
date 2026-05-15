import pandas as pd
import numpy as np

def prepare_sena_data(file_path):
   # 1. Load the dataset
    df = pd.read_csv(file_path)
    
    # 2. Filter by Virtual modality (Phase 2 of CRISP-ML)
    df_virtual = df[df['MODALIDAD_FORMACION'] == 'VIRTUAL'].copy()
    
    # 3. Convert dates to datetime format
    df_virtual['FECHA_INICIO_FICHA'] = pd.to_datetime(df_virtual['FECHA_INICIO_FICHA'], dayfirst=True)
    df_virtual['FECHA_TERMINACION_FICHA'] = pd.to_datetime(df_virtual['FECHA_TERMINACION_FICHA'], dayfirst=True)
    
    # 4. Feature Engineering: Course duration
    df_virtual['COURSE_DURATION_DAYS'] = (df_virtual['FECHA_TERMINACION_FICHA'] - df_virtual['FECHA_INICIO_FICHA']).dt.days
    
   # 5. Calculate Attrition Rate (Dropout Rate)
   # We avoid division by zero if a record has no enrolled students
    df_virtual['ATTRITION_RATE'] = (df_virtual['DESERTORES_AÑO_ACTUAL'] / df_virtual['TOTAL_APRENDICES_MATRICULADOS']).replace([np.inf, -np.inf], 0).fillna(0)
    
    # 6. Selection of final columns for the model
    final_features = [
        'NOMBRE_REGIONAL', 
        'NIVEL_FORMACION', 
        'TOTAL_APRENDICES_MATRICULADOS', 
        'COURSE_DURATION_DAYS',
        'ATTRITION_RATE' 
    ]
    
    return df_virtual[final_features]

# Example of use
if __name__ == "__main__":
    processed_data = prepare_sena_data('data/DESERCION_DE_LA_FORMACIÓN_PROFESIONAL_INTEGRAL_20260514.csv')
    print("Datos procesados exitosamente:")
    print(processed_data.head())
    
    # Save the clean dataset for the modeling phase
    processed_data.to_csv('data/sena_virtual_cleaned.csv', index=False)