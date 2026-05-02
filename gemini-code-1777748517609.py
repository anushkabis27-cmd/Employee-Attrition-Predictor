import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

# Set page config
st.set_page_config(page_title="Attrition AI Predictor", layout="wide")

# --- DATA ENGINE ---
@st.cache_data
def load_and_process():
    df = pd.read_csv('final_attrition_dataset_500_v4_lateral.csv')
    
    # Simple encoding for the model
    le = LabelEncoder()
    df['GRADE_ID'] = le.fit_transform(df['GRADE'])
    df['GROUP_ID'] = le.fit_transform(df['MAIN_GROUP'])
    df['ZONE_ID'] = le.fit_transform(df['ZONE'])
    
    X = df[['AGE', 'TENURE_YRS', 'GRADE_ID', 'GROUP_ID', 'ZONE_ID']]
    y = df['ATTRITION']
    
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X, y)
    
    df['Risk_Score'] = (rf.predict_proba(X)[:, 1] * 100).round(2)
    df['Is_High_Risk'] = df['Risk_Score'] >= 75
    return df

df = load_and_process()

# --- NAVIGATION ---
page = st.sidebar.selectbox("Navigate", ["Zone & Group Analytics", "Employee Search"])

# --- PAGE 1: ZONE & GROUP ANALYTICS ---
if page == "Zone & Group Analytics":
    st.title("🌍 Regional High-Risk Analysis")
    st.markdown("Percentage of employees with a **75% or higher** risk of attrition.")
    
    # Calculate Group % per Zone
    report = df.groupby(['ZONE', 'MAIN_GROUP'])['Is_High_Risk'].mean() * 100
    report = report.unstack().fillna(0).round(2)
    
    # Display Zones
    zones = ["North", "East", "West", "South"]
    cols = st.columns(4)
    
    for i, zone in enumerate(zones):
        with cols[i]:
            st.subheader(f"📍 {zone} Zone")
            if zone in report.index:
                st.dataframe(report.loc[zone].rename("High Risk %"))
            else:
                st.write("No data for this zone.")

# --- PAGE 2: EMPLOYEE SEARCH ---
elif page == "Employee Search":
    st.title("🔍 Individual Risk Profile")
    
    emp_id = st.number_input("Enter Employee ID", min_value=0, step=1)
    
    if emp_id:
        user_data = df[df['EMPID'] == emp_id]
        
        if not user_data.empty:
            score = user_data['Risk_Score'].values[0]
            
            # Big Score Display
            color = "red" if score >= 75 else "orange" if score >= 40 else "green"
            st.markdown(f"<h1 style='text-align: center; color: {color}; font-size: 80px;'>{score}%</h1>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center;'>Predicted Attrition Risk</p>", unsafe_allow_html=True)
            
            st.divider()
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📝 Reasons for Risk")
                if score >= 75:
                    st.write("* **Critical Tenure:** Within the high-churn 3-5 year bracket.")
                    st.write(f"* **Grade Vulnerability:** Current Grade ({user_data['GRADE'].values[0]}) shows high exit volatility.")
                    st.write("* **Regional Trend:** Similar exits observed in the current business group.")
                else:
                    st.write("* **Stable Tenure:** Employee has moved past the high-risk 3-year mark.")
                    st.write("* **Career Growth:** Grade and Age profile matches historical 'Loyal' segments.")

            with col2:
                st.subheader("🚀 Actionables for ER Manager")
                if score >= 75:
                    st.write("* **Immediate Outreach:** ER manager should schedule a 1-on-1 to understand career frustrations.")
                    st.write("* **Retention Bonus:** Evaluate eligibility for a stay-bonus or performance incentive.")
                    st.write("* **Role Rotation:** Explore lateral movement within other groups to renew interest.")
                else:
                    st.write("* **Monitor:** Continue standard quarterly reviews.")
                    st.write("* **Mentorship:** Potential candidate to mentor newer hires in the DM/M grades.")
        else:
            st.error("Employee ID not found in the database.")