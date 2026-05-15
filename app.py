import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# --- 1. MUST BE THE FIRST STREAMLIT COMMAND ---
st.set_page_config(page_title="iRetain | Predictive Insights", layout="wide") [cite: 1]

# --- 2. FUTURISTIC iRETAIN THEME ---
st.markdown("""
    <style>
    .main { background-color: #0A192F; color: #E6F1FF; }
    [data-testid="stSidebar"] { background-color: #f37021; border-right: 2px solid #003366; }
    [data-testid="stSidebar"] .st-emotion-cache-10trblm { color: white; }
    .stMetric { background-color: #112240; padding: 20px; border-radius: 15px; border: 1px solid #233554; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }
    h1, h2 { color: #64FFDA; font-family: 'Arial'; text-shadow: 2px 2px 4px #000; font-weight: bold; }
    h3 { color: #f37021; font-weight: bold; }
    .risk-box { padding: 30px; border-radius: 20px; text-align: center; border: 2px solid; background: rgba(0,0,0,0.3); margin-bottom: 25px; }
    .big-font { font-size: 85px !important; font-weight: bold; }
    .report-card { background: rgba(17, 34, 64, 0.9); padding: 25px; border-radius: 15px; border-left: 5px solid #f37021; margin-bottom: 20px; min-height: 250px; }
    .profile-text { font-size: 18px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True) [cite: 1, 2, 3, 4, 5]

# --- 3. DATA LOADER ---
@st.cache_data
def load_data():
    file_path = 'Attrition.csv'
    if not os.path.exists(file_path):
        st.error(f"⚠️ **File Not Found:** Please ensure '{file_path}' is in the repository.")
        st.stop()
    try:
        df = pd.read_csv(file_path) [cite: 6]
        df.columns = df.columns.str.strip() [cite: 6]
        if 'Status' in df.columns:
            active_df = df[df['Status'].str.upper() == 'ACTIVE'].copy() [cite: 6]
        else:
            active_df = df.copy() [cite: 7]
        return active_df
    except Exception as e:
        st.error(f"❌ **Error reading file:** {e}")
        st.stop()

df = load_data()

# --- 4. STATE MANAGEMENT ---
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = "Zone wise turnover prediction"
if 'selected_empid' not in st.session_state:
    st.session_state['selected_empid'] = None

# --- 5. SIDEBAR NAVIGATION ---
st.sidebar.title("💠 iRETAIN ENGINE")
st.sidebar.markdown("---")
page_options = ["Zone wise turnover prediction", "Employee risk indicator", "ER Login"]
selected_page = st.sidebar.radio("NAVIGATION", page_options, 
                                  index=page_options.index(st.session_state['current_page']))
st.session_state['current_page'] = selected_page

# --- PAGE 1: ZONE WISE TURNOVER PREDICTION ---
if st.session_state['current_page'] == "Zone wise turnover prediction":
    st.title("🌐 Zone wise turnover prediction")
    region_col = 'ZONE' if 'ZONE' in df.columns else ('Home State' if 'Home State' in df.columns else None) [cite: 8, 9]
    if region_col:
        regions = df[region_col].unique()[:4] [cite: 9]
        cols = st.columns(2) [cite: 9]
        for i, region in enumerate(regions):
            with cols[i % 2]:
                st.markdown(f"<div class='stMetric'><h3>📍 {region}</h3>", unsafe_allow_html=True) [cite: 9, 10]
                reg_df = df[df[region_col] == region] [cite: 10]
                level_col = 'Risk_Level' if 'Risk_Level' in df.columns else 'Risk Level' [cite: 10]
                counts = reg_df[level_col].value_counts(normalize=True) * 100 [cite: 10]
                fig, ax = plt.subplots(figsize=(6, 3)) [cite: 11]
                cats = ['High', 'Medium', 'Low'] [cite: 11]
                vals = [counts.get('High', 0), counts.get('Medium', 0), counts.get('Low', 0)] [cite: 11]
                bars = ax.bar(cats, vals, color=['#FF3131', '#FFD700', '#2ECC71'], edgecolor='white') [cite: 12]
                ax.set_facecolor('#112240') [cite: 12]
                fig.patch.set_facecolor('#0A192F') [cite: 12]
                ax.tick_params(colors='white') [cite: 12]
                ax.set_ylim(0, 100) [cite: 12]
                st.pyplot(fig) [cite: 14]
                st.markdown("</div>", unsafe_allow_html=True) [cite: 14]

# --- PAGE 2: EMPLOYEE RISK INDICATOR ---
elif st.session_state['current_page'] == "Employee risk indicator":
    st.title("🆔 Employee risk indicator")
    if st.session_state['selected_empid']:
        emp_id = st.session_state['selected_empid']
        if st.button("⬅️ Back to ER Dashboard"):
            st.session_state['selected_empid'] = None
            st.session_state['current_page'] = "ER Login"
            st.rerun()
    else:
        emp_id = st.number_input("Enter EMPID to search", min_value=0, step=1) [cite: 14]

    if emp_id:
        user_data = df[df['EMPID'] == emp_id] [cite: 15]
        if not user_data.empty: [cite: 15]
            row = user_data.iloc[0] [cite: 15]
            score = row.get('Attrition_Risk_Percentage', 0) [cite: 16]
            level = row.get('Risk_Level', 'Low') [cite: 16]
            h_color = "#FF3131" if level == 'High' else ("#FFD700" if level == 'Medium' else "#2ECC71") [cite: 16]
            st.markdown(f"<div class='risk-box' style='border-color: {h_color};'>", unsafe_allow_html=True) [cite: 16]
            st.markdown(f"<p class='big-font' style='color: {h_color};'>{score}%</p>", unsafe_allow_html=True) [cite: 17]
            st.markdown(f"<h1 style='color: {h_color};'>{level.upper()} RISK</h1>", unsafe_allow_html=True) [cite: 17]
            st.markdown("</div>", unsafe_allow_html=True) [cite: 17]
            
            st.subheader("📋 Employee Profile Details") [cite: 18]
            c1, c2, c3 = st.columns(3) [cite: 18]
            with c1:
                st.write(f"**Grade:** {row.get('GRADE', 'N/A')}") [cite: 18]
                st.write(f"**EMPID:** {row.get('EMPID', 'N/A')}") [cite: 18]
            with c2:
                st.write(f"**Age:** {row.get('AGE', 'N/A')}") [cite: 19]
                st.write(f"**Tenure:** {row.get('TENURE_YRS', 'N/A')} Years") [cite: 19]
            with c3:
                st.write(f"**Zone:** {row.get('ZONE', 'N/A')}") [cite: 19]
                st.write(f"**Work City:** {row.get('Work_Location', 'N/A')}") [cite: 19]

            col_a, col_b = st.columns(2) [cite: 20]
            with col_a:
                st.markdown("<div class='report-card'><h4>🔍 Risk Factor Analysis</h4>", unsafe_allow_html=True) [cite: 20]
                if level == 'High': [cite: 21]
                    st.write("• Profile within Critical Attrition Window (3-5 years).") [cite: 21]
                    st.write("• Distance/Tenure ratio suggests immediate risk.") [cite: 21]
                elif level == 'Medium': [cite: 22]
                    st.write("• Mid-tenure engagement dip detected.") [cite: 22]
                else:
                    st.write("• Stable organizational anchoring.") [cite: 22, 23]
                st.markdown("</div>", unsafe_allow_html=True) [cite: 23]
            with col_b:
                st.markdown(f"<div class='report-card' style='border-left-color: {h_color};'><h4>🚀 Mitigation Actionables</h4>", unsafe_allow_html=True) [cite: 23]
                if level == 'High': [cite: 24]
                    st.write("• **ER Intervention:** Urgent 1:1 visit required.") [cite: 24]
                    st.write("• **Retention Plan:** Relationship Reset & Mentorship.") [cite: 24]
                elif level == 'Medium': [cite: 25]
                    st.write("• **Structured Connect:** ER Manager confidential 1:1.") [cite: 25]
                else:
                    st.write("• **Appreciation:** Nominate for performance award.") [cite: 25, 26]
                st.markdown("</div>", unsafe_allow_html=True) [cite: 26]
        else:
            st.error("EMPID not found.") [cite: 26]

# --- PAGE 3: ER LOGIN ---
elif st.session_state['current_page'] == "ER Login":
    st.title("👤 ER Manager Portal")
    er_id = st.number_input("Enter ER Manager ID", min_value=0, step=1)
    if er_id:
        if 'ER manager ID' in df.columns and er_id in df['ER manager ID'].values:
            manager_df = df[df['ER manager ID'] == er_id]
            high_risk_df = manager_df[manager_df['Risk_Level'] == 'High']
            st.metric("Total High Risk Employees Mapped", len(high_risk_df))
            if st.button("🔍 View High Risk Employee List"):
                st.session_state['show_er_list'] = True
            if st.session_state.get('show_er_list'):
                for _, row in high_risk_df.iterrows():
                    c1, c2, c3 = st.columns([1, 1, 1])
                    c1.write(f"**EMPID:** {row['EMPID']}")
                    c2.write(f"**Risk:** {row['Attrition_Risk_Percentage']}%")
                    if c3.button("Analyze", key=f"er_{row['EMPID']}"):
                        st.session_state['selected_empid'] = row['EMPID']
                        st.session_state['current_page'] = "Employee risk indicator"
                        st.rerun()
        else:
            st.error("Manager ID not found.")
