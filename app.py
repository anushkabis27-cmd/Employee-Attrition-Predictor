import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(page_title="ICICI Turnover Predictor", layout="wide")

# 2. Data Loading (MUST BE OUTSIDE OF NAVIGATION LOGIC)
@st.cache_data
def load_data():
    # Make sure this filename matches exactly what is in your GitHub repo
    data = pd.read_excel("Attrition_Final_Production.xlsx")
    return data

# This defines 'df' globally for the whole app
df = load_data() 

# 3. Navigation State Management
if 'page' not in st.session_state:
    st.session_state.page = 'Overview'

# ... (rest of your navigation buttons and Page 1/Page 2 logic)
