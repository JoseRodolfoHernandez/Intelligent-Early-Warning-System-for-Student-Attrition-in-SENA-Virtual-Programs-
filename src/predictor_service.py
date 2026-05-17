import os
import pandas as pd
import joblib
import streamlit as st

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@st.cache_resource
def load_assets():
    model_path = os.path.join(BASE_DIR, 'attrition_model.pkl')
    columns_path = os.path.join(BASE_DIR, 'model_columns.pkl')
    return joblib.load(model_path), joblib.load(columns_path)

def run_prediction_ui():
    st.title(" Early Warning System: Student Attrition")
    st.markdown("Predict the risk of dropout for SENA Virtual Programs.")

    try:
        model, model_columns = load_assets()

        # Inputs
        st.sidebar.header("Course Parameters")
        regional = st.sidebar.selectbox("Regional Name", ["REGIONAL BOGOTA", "REGIONAL ANTIOQUIA", "REGIONAL VALLE", "REGIONAL ATLANTICO"])
        nivel = st.sidebar.selectbox("Training Level", ["TECNOLOGO", "TECNICO", "CURSO ESPECIAL"])
        matriculados = st.sidebar.slider("Total Enrolled Students", 1, 150, 50)
        duracion = st.sidebar.number_input("Course Duration (Days)", min_value=1, value=365)

        if st.button("Predict Attrition Risk"):
            input_dict = {
                'NOMBRE_REGIONAL': regional,
                'NIVEL_FORMACION': nivel,
                'TOTAL_APRENDICES_MATRICULADOS': matriculados,
                'DURATION_DAYS': duracion
            }
            
            # Data transformation logic
            input_df = pd.get_dummies(pd.DataFrame([input_dict]))
            for col in model_columns:
                if col not in input_df.columns:
                    input_df[col] = 0
            input_df = input_df[model_columns]
            
            prediction = model.predict(input_df)[0]
            
            # UI Output logic
            st.subheader("Prediction Result")
            risk_color = "red" if prediction > 0.20 else "orange" if prediction > 0.10 else "green"
            st.markdown(f"### Estimated Attrition Rate: :{risk_color}[{prediction:.2%}]")
            
            if prediction > 0.20:
                st.error(" HIGH RISK: Immediate pedagogical intervention recommended.")
            else:
                st.success(" STABLE: Normal monitoring levels.")

    except Exception as e:
        st.error(f"Error executing prediction engine: {e}")