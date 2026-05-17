import streamlit as st
import os
from predictor_service import run_prediction_ui

# Page Setup
st.set_page_config(page_title="SENA Attrition Predictor", page_icon="🎓")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

# ROUTER: Define the visual tabs (Paths)
tab1, tab2 = st.tabs([" Predictive System", " Business & Data Understanding"])

# ROUTE 1: Render Predictive Model View
with tab1:
    run_prediction_ui()

# ROUTE 2: Render Documentation Template View
with tab2:
    template_path = os.path.join(PROJECT_ROOT, 'templates', 'business_understanding.md')
    
    if os.path.exists(template_path):
        with open(template_path, 'r', encoding='utf-8') as file:
            markdown_content = file.read()
        st.markdown(markdown_content)
    else:
        st.error("Technical Documentation template not found.")