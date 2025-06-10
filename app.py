import os
import pickle
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import time
import base64
from datetime import datetime
import json

# Set page configuration
st.set_page_config(
    page_title="Health Assistant Pro",
    layout="wide",
    page_icon="🧑‍⚕️",
    initial_sidebar_state="expanded"
)

# Custom CSS with more styling
st.markdown("""
    <style>
    .main {
        padding: 20px;
    }
    .stButton>button {
        width: 100%;
        background-color: #ff4b4b;
        color: white;
        padding: 10px;
        border-radius: 10px;
        border: none;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #ff6b6b;
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    .sidebar .sidebar-content {
        background-color: #f0f2f6;
    }
    .st-emotion-cache-1wmy9hl {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 20px;
        border-radius: 10px;
    }
    h1 {
        color: #1e3d59;
        text-align: center;
        padding: 20px;
        border-bottom: 2px solid #ff6b6b;
        margin-bottom: 30px;
    }
    .stTextInput>div>div>input {
        background-color: #ffffff;
        border-radius: 5px;
        border: 1px solid #e0e0e0;
        padding: 10px;
    }
    .tooltip {
        position: relative;
        display: inline-block;
        border-bottom: 1px dotted #ccc;
        cursor: help;
    }
    .tooltip .tooltiptext {
        visibility: hidden;
        width: 200px;
        background-color: #555;
        color: #fff;
        text-align: center;
        border-radius: 6px;
        padding: 5px;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        margin-left: -100px;
        opacity: 0;
        transition: opacity 0.3s;
    }
            /* Add to your existing CSS */
.stButton>button {
    background-color: #1e3d59 !important;  
    color: white !important;
    border: 2px solid #ff4b4b !important;
}

.stButton>button:hover {
    background-color: #ff4b4b !important;
    border-color: #1e3d59 !important;
}

h1 {
    color: #1e3d59 !important; 
}

.custom-container {
    border-left: 4px solid #1e3d59;  
}


[data-testid="stSidebar"] {
    box-shadow: 2px 0 5px rgba(0,0,0,0.1);
}
    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }
    .custom-container {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
             .sidebar .sidebar-content {
52        background: linear-gradient(180deg, #1e3d59 0%, #2e5d79 100%);
53    }
54    
55    [data-testid="stSidebar"] {
56        background-color: #1e3d59;
57        border-right: 2px solid #ff4b4b;
58    }
59    
60    [data-testid="stSidebar"] > div:first-child {
61        padding-top: 2rem;
62        padding-bottom: 2rem;
63    }
64    
65    .sidebar-title {
66        color: #ffffff !important;
67        text-align: center;
68        margin-bottom: 40px;
69        padding: 20px 0;
70        border-bottom: 2px solid #ff4b4b;
71    }
72    
73    .sidebar .sidebar-content .stMarkdown {
74        color: #ffffff;
75    }
76    
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if 'history' not in st.session_state:
    st.session_state.history = []

# Load the model
model_path = r"diabetes_model.sav"
if not os.path.exists(model_path):
    st.error("Model file not found! Please check the file path.")
try:
    diabetes_model = pickle.load(open(model_path, "rb"))
    if not hasattr(diabetes_model, 'predict'):
        st.error("Invalid model file! The loaded object doesn't have prediction capability.")
except Exception as e:
    st.error(f"Error loading model: {str(e)}")

# Helper functions
def create_tooltip(text, help_text):
    return f'<div class="tooltip">{text}<span class="tooltiptext">{help_text}</span></div>'

def save_prediction(data, prediction):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    result = {
        "timestamp": timestamp,
        "data": data,
        "prediction": int(prediction[0])
    }
    st.session_state.history.append(result)

def download_results():
    df = pd.DataFrame(st.session_state.history)
    return df.to_csv(index=False)

def create_gauge_chart(value, title, min_val, max_val, normal_range):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = value,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': title},
        gauge = {
            'axis': {'range': [min_val, max_val]},
            'bar': {'color': "#ff4b4b"},
            'steps': [
                {'range': normal_range, 'color': "lightgreen"}
            ]
        }
    ))
    return fig

# Sidebar
# Sidebar
with st.sidebar:
    selected = option_menu(
        menu_title='Health Prediction System',
        options=['Home', 'Diabetes Prediction', 'History', 'Help'],
        icons=['house', 'activity', 'clock-history', 'question-circle'],
        menu_icon='hospital-fill',
        default_index=0,
        styles={
            "container": {"padding": "5!important", "background-color": "#0E1117"},
            "icon": {"color": "#ff4b4b", "font-size": "25px"}, 
            "nav-link": {
                "font-size": "16px", 
                "text-align": "left", 
                "margin": "0px", 
                "--hover-color": "#2e5d79",
                "color": "#ff4b4b"  
            },
            "nav-link-selected": {
                "background-color": "#ffffff",
                "color": "#1e3d59",
            },
            "icon-selected": {
                "color": "#1e3d59"
            },
            "menu-title": {  # Added this style
                "color": "#ffffff"
            }
        }
    )

# Home Page
if selected == 'Home':
    st.title('Welcome to Health Assistant Pro')
    
    st.markdown("""
    ### 🌟 Features
    - Advanced Diabetes Prediction
    - Real-time Health Monitoring
    - Historical Data Analysis
    - Expert Recommendations
    
    ### 🎯 How to Use
    1. Navigate to the Diabetes Prediction page
    2. Enter your health parameters
    3. Get instant predictions and recommendations
    4. Track your history over time
    """)

# Diabetes Prediction Page
elif selected == 'Diabetes Prediction':
    st.title('Diabetes Prediction using ML')
    
    # Tutorial
    if st.checkbox('Show Tutorial'):
        st.info("""
        ### Quick Tutorial:
        1. Fill in all the required health parameters
        2. Click the 'Predict' button
        3. Review your results and recommendations
        4. Save or download your results for future reference
        """)

    # Main prediction interface
    left_column, right_column = st.columns([2, 1])
    
    with left_column:
        with st.form("prediction_form"):
            st.subheader("Enter Patient Details")
            
            col1, col2, col3 = st.columns(3)

            with col1:
                Pregnancies = st.number_input('Number of Pregnancies', 
                    min_value=0, max_value=20, value=0,
                    help="Number of times pregnant")
                
                SkinThickness = st.number_input('Skin Thickness', 
                    min_value=0, max_value=100, value=0,
                    help="Triceps skin fold thickness (mm)")
                
                DiabetesPedigreeFunction = st.number_input('Diabetes Pedigree Function',
                    min_value=0.0, max_value=3.0, value=0.0,
                    help="Diabetes pedigree function (a function which scores likelihood of diabetes based on family history)")

            with col2:
                Glucose = st.number_input('Glucose Level',
                    min_value=0, max_value=200, value=0,
                    help="Plasma glucose concentration after 2 hours in an oral glucose tolerance test")
                
                Insulin = st.number_input('Insulin Level',
                    min_value=0, max_value=846, value=0,
                    help="2-Hour serum insulin (mu U/ml)")
                
                Age = st.number_input('Age',
                    min_value=0, max_value=120, value=0,
                    help="Age in years")

            with col3:
                BloodPressure = st.number_input('Blood Pressure',
                    min_value=0, max_value=122, value=0,
                    help="Diastolic blood pressure (mm Hg)")
                
                BMI = st.number_input('BMI',
                    min_value=0.0, max_value=67.1, value=0.0,
                    help="Body mass index (weight in kg/(height in m)^2)")

            submitted = st.form_submit_button("Predict")

    with right_column:
        st.markdown("""
        ### Reference Ranges
        
        - **Glucose:** 70-140 mg/dL
        - **Blood Pressure:** 60-80 mm Hg
        - **BMI:** 18.5-24.9
        - **Insulin:** 16-166 mU/L
        """)

    if submitted:
        # Show progress bar
        progress_bar = st.progress(0)
        for i in range(100):
            time.sleep(0.01)
            progress_bar.progress(i + 1)

        user_input = [Pregnancies, Glucose, BloodPressure, SkinThickness, 
                     Insulin, BMI, DiabetesPedigreeFunction, Age]
        
        # Input validation
        if any(x < 0 for x in user_input):
            st.warning("Please ensure all values are non-negative.")
        else:
            try:
                diab_prediction = diabetes_model.predict([user_input])
                save_prediction(user_input, diab_prediction)

                # Display results
                st.markdown("## Results")
                col1, col2 = st.columns(2)

                with col1:
                    if diab_prediction[0] == 1:
                        st.error('⚠️ High Risk of Diabetes Detected')
                    else:
                        st.success('✅ Low Risk of Diabetes Detected')

                # Display gauge charts
                st.subheader("Key Metrics")
                col1, col2, col3 = st.columns(3)

                with col1:
                    fig1 = create_gauge_chart(Glucose, "Glucose", 0, 200, [70, 140])
                    st.plotly_chart(fig1)

                with col2:
                    fig2 = create_gauge_chart(BMI, "BMI", 0, 50, [18.5, 24.9])
                    st.plotly_chart(fig2)

                with col3:
                    fig3 = create_gauge_chart(BloodPressure, "Blood Pressure", 0, 122, [60, 80])
                    st.plotly_chart(fig3)

                # Recommendations
                st.subheader("Recommendations")
                if diab_prediction[0] == 1:
                    st.markdown("""
                    1. 🏥 **Consult a Healthcare Provider Immediately**
                    2. 📊 **Monitor Blood Sugar Regularly**
                    3. 🥗 **Follow a Diabetes-Friendly Diet**
                    4. 🏃‍♂️ **Engage in Regular Physical Activity**
                    5. 💊 **Discuss Medication Options with Your Doctor**
                    """)
                else:
                    st.markdown("""
                    1. 🥗 **Maintain a Balanced Diet**
                    2. 🏃‍♂️ **Regular Exercise (30 mins/day)**
                    3. ⚖️ **Maintain Healthy Weight**
                    4. 🏥 **Regular Health Check-ups**
                    5. 😴 **Ensure Adequate Sleep**
                    """)

                # Download results
                st.download_button(
                    label="Download Results",
                    data=download_results(),
                    file_name="diabetes_prediction_results.csv",
                    mime="text/csv"
                )

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

elif selected == 'History':
    st.title('Prediction History')
    
    if st.session_state.history:
        df = pd.DataFrame(st.session_state.history)
        st.dataframe(df)
        
        # Visualizations
        st.subheader("Trends Over Time")
        fig = px.line(df, x='timestamp', y='prediction', title='Prediction Results Over Time')
        st.plotly_chart(fig)
    else:
        st.info("No prediction history available yet.")

elif selected == 'Help':
    st.title('Help & FAQ')
    
    faq_data = {
        "What is diabetes?": "Diabetes is a chronic condition that affects how your body turns food into energy.",
        "How accurate is the prediction?": "The model's accuracy is based on training data and should be used as a screening tool, not a final diagnosis.",
        "What should I do if I get a positive result?": "Consult with a healthcare provider immediately for proper diagnosis and treatment.",
        "How often should I get tested?": "It's recommended to get tested at least once a year if you have risk factors for diabetes."
    }
    
    for question, answer in faq_data.items():
        with st.expander(question):
            st.write(answer)
    
    st.markdown("""
    🔗 Resources:
    - [American Diabetes Association](https://www.diabetes.org/)
    - [WHO Diabetes Information](https://www.who.int/health-topics/diabetes)
    """)

# Footer
st.markdown("""
---
<div style='text-align: center'>
    <p>© 2024 Health Assistant Pro. All rights reserved.</p>
    <p>Disclaimer: This tool is for educational purposes only and should not be used as a substitute for professional medical advice.</p>
</div>
""", unsafe_allow_html=True)
