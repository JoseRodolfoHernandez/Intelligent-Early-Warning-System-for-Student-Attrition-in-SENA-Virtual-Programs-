import streamlit as st
import os
from streamlit_option_menu import option_menu
from predictor_service import run_prediction_ui

# 1. Page Configuration
st.set_page_config(page_title="SENA Core Analytics", page_icon="🎓", layout="wide")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

# 2. Main Navigation Menu & Submenus (Sidebar Architecture)
with st.sidebar:
    st.markdown("## ⚙️ Core Navigation")
    selected_menu = option_menu(
        menu_title="Project Lifecycle",
        options=["Prediction Engine", "Business Framework", "Data & Modeling", "MLOps & Deployment"],
        icons=["cpu", "briefcase", "bezier2", "cloud-arrow-up"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "5px!", "background-color": "#1e222b"},
            "icon": {"color": "#00ffcc", "font-size": "18px"}, 
            "nav-link": {"font-size": "14px", "text-align": "left", "margin":"0px", "--hover-color": "#282c34"},
            "nav-link-selected": {"background-color": "#00a381"},
        }
    )

# 3. ROUTER CHANNELS (Executing paths based on selection)
if selected_menu == "Prediction Engine":
    # Route to Core Predictive Microservice
    run_prediction_ui()

elif selected_menu == "Business Framework":
    # Route to Business Understanding Specification
    template_path = os.path.join(PROJECT_ROOT, 'templates', 'business_understanding.md')
    with open(template_path, 'r', encoding='utf-8') as file:
        st.markdown(file.read())

elif selected_menu == "Data & Modeling":
    # Route to Data Engineering Documentation
    template_path = os.path.join(PROJECT_ROOT, 'templates', 'data_preparation.md')
    with open(template_path, 'r', encoding='utf-8') as file:
        st.markdown(file.read())

elif selected_menu == "MLOps & Deployment":
    # Route to Infrastructure & Monitoring Protocols
    template_path = os.path.join(PROJECT_ROOT, 'templates', 'deployment_monitoring.md')
    with open(template_path, 'r', encoding='utf-8') as file:
        st.markdown(file.read())