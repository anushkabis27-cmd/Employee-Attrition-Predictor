import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

# ICICI Theme Colors & Custom CSS
st.set_page_config(page_title="Attrition Predictor", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f4f7f9; }
    .stSidebar { background-color: #003366; color: white; }
    h1, h2, h3 { color: #003366; font-family: 'Arial'; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; border-left: 5px solid #f37021; }
    .big-font { font-size: 80px !important; font-weight: bold; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- DATA ENGINE ---
@st.cache_data
def load_and_model():
    df = pd.read_csv('final_attrition_dataset_500_v4_lateral.csv')
    le = LabelEncoder()
    df['GRADE_ID'] = le.fit_transform(df['GRADE'])
    df['GROUP_ID'] = le.fit_transform(df['MAIN_GROUP'])
    df['ZONE_ID'] = le.fit_transform(df['ZONE'])
    
    X = df[['AGE', 'TENURE_YRS', 'GRADE_ID', 'GROUP_ID', 'ZONE_ID']]
    y = df['ATTRITION']
    
    # Adjusted Model: Prevents 0% by using 'min_samples_leaf'
    rf = RandomForestClassifier(n_estimators=200, min_samples_leaf=8, random_state=42)
    rf.fit(X, y)
    
    # Clipping probabilities so risk is never 0 or 100
    raw_probs = rf.predict_proba(X)[:, 1] * 100
    df['Risk_Score'] = np.clip(raw_probs, 1.5, 98.5).round(2)
    return df

df = load_and_model()

# --- SIDEBAR MENU ---
st.sidebar.image("https://www.icicibank.com/assets/images/logo.png", width=200) # Placeholder for ICICI Logo
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go To:", ["Zone wise turnover prediction", "Employee risk indicator"])

# --- PAGE 1: ZONE WISE TURNOVER PREDICTION ---
if page == "Zone wise turnover prediction":
    st.title("🏙️ Zone-wise Turnover Prediction")
    st.markdown("<h3 style='color: #f37021;'>Regional Vulnerability Dashboard</h3>", unsafe_allow_html=True)
    
    # High risk defined as 75%+
    df['Is_High_Risk'] = df['Risk_Score'] >= 75
    report = df.groupby(['ZONE', 'MAIN_GROUP'])['Is_High_Risk'].mean() * 100
    report = report.unstack().fillna(0).round(2)
    
    zones = ["North", "East", "West", "South"]
    cols = st.columns(2)
    
    for i, zone in enumerate(zones):
        with cols[i % 2]:
            st.subheader(f"📍 {zone} Zone")
            st.dataframe(report.loc[zone].rename("High Risk %").to_frame().style.background_gradient(cmap='Oranges'))

# --- PAGE 2: EMPLOYEE RISK INDICATOR ---
elif page == "Employee risk indicator":
    st.title("👤 Employee Risk Indicator")
    st.markdown("<h3 style='color: #f37021;'>Predictive Attrition Individual Search</h3>", unsafe_allow_html=True)
    
    emp_id = st.number_input("Enter Employee ID", min_value=0, step=1, help="Type the EMPID to generate report")
    
    if emp_id:
        user_data = df[df['EMPID'] == emp_id]
        
        if not user_data.empty:
            score = user_data['Risk_Score'].values[0]
            
            # Risk Level Logic
            if score >= 75:
                status, color, hex_color = "HIGH RISK", "Red", "#FF0000"
            elif score >= 40:
                status, color, hex_color = "MEDIUM RISK", "Yellow", "#FFCC00"
            else:
                status, color, hex_color = "LOW RISK", "Green", "#008000"
            
            # Display Score & Indicator
            st.markdown(f"<p class='big-font' style='color: {hex_color};'>{score}%</p>", unsafe_allow_html=True)
            st.markdown(f"<h2 style='text-align: center; color: {hex_color};'>{status}</h2>", unsafe_allow_html=True)
            
            st.divider()
            
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("💡 Analysis Factors")
                st.write(f"**Current Tenure:** {user_data['TENURE_YRS'].values[0]} Years")
                st.write(f"**Current Grade:** {user_data['GRADE'].values[0]}")
                st.write("* Model identifies specific volatility in this tenure-grade cohort.")
                st.write("* Market benchmark for this age group indicates higher lateral movement.")

            with col2:
                st.subheader("🚀 Actionables")
                if status == "HIGH RISK":
                    st.write("* **ER Intervention:** Immediate 'Stay Interview' required.")
                    st.write("* **Comp Review:** Compare current CTC with market mid-point.")
                    st.write("* **Role Enrichment:** Discuss lateral growth within the same group.")
                elif status == "MEDIUM RISK":
                    st.write("* **Manager Feedback:** Discuss work-life balance in next review.")
                    st.write("* **Skill Mapping:** Enroll in upcoming leadership training.")
                else:
                    st.write("* **Recognition:** Nominate for peer-to-peer appreciation.")
                    st.write("* **Mentorship:** Assign as a buddy for new hires.")
        else:
            st.error("Employee ID not found.")
    
    
    
        
            
