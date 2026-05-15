import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# --- FUTURISTIC ICICI THEME CONFIG ---
st.set_page_config(page_title="ICICI Attrition Predictor", layout="wide")

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
    .list-row { background: #112240; padding: 10px; border-radius: 10px; margin-bottom: 5px; border: 1px solid #233554; }
    </style>
    """, unsafe_allow_html=True)

# --- ROBUST DATA LOADER ---
@st.cache_data
def load_data():
    file_path = 'Attrition.csv'
    if not os.path.exists(file_path):
        st.error(f"⚠️ **File Not Found:** Please upload '{file_path}'")
        st.stop()
    try:
        df = pd.read_excel(file_path, sheet_name=0)
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        st.error(f"❌ **Error:** {e}")
        st.stop()

df = load_data()

# --- STATE MANAGEMENT ---
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = "Zone wise turnover prediction"
if 'selected_empid' not in st.session_state:
    st.session_state['selected_empid'] = None

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("💠 iRetain")
st.sidebar.markdown("---")

# Sync sidebar with session state
page_options = ["Zone wise turnover prediction", "Employee risk indicator", "ER Login"]
selected_page = st.sidebar.radio("NAVIGATION", page_options, 
                                  index=page_options.index(st.session_state['current_page']))
st.session_state['current_page'] = selected_page

# --- PAGE 1: ZONE WISE TURNOVER PREDICTION ---
if st.session_state['current_page'] == "Zone wise turnover prediction":
    st.title("🌐 Zone wise turnover prediction [cite: 8]")
    st.markdown("#### Regional Vulnerability Matrix [cite: 8]")
    
    region_col = 'Home State' if 'Home State' in df.columns else ('ZONE' if 'ZONE' in df.columns else None)
    if region_col:
        regions = df[region_col].unique()[:4]
        cols = st.columns(2) [cite: 9]
        for i, region in enumerate(regions):
            with cols[i % 2]:
                st.markdown(f"<div class='stMetric'><h3>📍 {region}</h3>", unsafe_allow_html=True)
                reg_df = df[df[region_col] == region]
                level_col = 'Risk_Level' if 'Risk_Level' in df.columns else 'Risk Level'
                counts = reg_df[level_col].value_counts(normalize=True) * 100
                
                fig, ax = plt.subplots(figsize=(6, 3)) [cite: 11]
                cats = ['High', 'Medium', 'Low']
                vals = [counts.get('High', 0), counts.get('Medium', 0), counts.get('Low', 0)]
                bars = ax.bar(cats, vals, color=['#FF3131', '#FFD700', '#2ECC71'], edgecolor='white') [cite: 12]
                ax.set_facecolor('#112240')
                fig.patch.set_facecolor('#0A192F')
                ax.tick_params(colors='white')
                ax.set_ylim(0, 100)
                for bar in bars:
                    ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 2, f'{bar.get_height():.1f}%', ha='center', color='#64FFDA', fontweight='bold') [cite: 13]
                st.pyplot(fig)
                st.markdown("</div>", unsafe_allow_html=True)

# --- PAGE 2: EMPLOYEE RISK INDICATOR ---
elif st.session_state['current_page'] == "Employee risk indicator":
    st.title("🆔 Employee risk indicator [cite: 15]")
    
    # Check if we arrived here from ER Login via a specific EMPID
    if st.session_state['selected_empid']:
        emp_id = st.session_state['selected_empid']
        if st.button("⬅️ Back to ER Dashboard"):
            st.session_state['selected_empid'] = None
            st.session_state['current_page'] = "ER Login"
            st.rerun()
    else:
        emp_id = st.number_input("Enter EMPID to search", min_value=0, step=1) [cite: 15]

    if emp_id:
        user_data = df[df['EMPID'] == emp_id]
        if not user_data.empty:
            row = user_data.iloc[0]
            score = row.get('Attrition_Risk_Percentage', row.get('Attrition Risk (%)', 0)) [cite: 16]
            level = row.get('Risk_Level', row.get('Risk Level', 'Low'))
            h_color = "#FF3131" if level == 'High' else ("#FFD700" if level == 'Medium' else "#2ECC71")
            
            st.markdown(f"<div class='risk-box' style='border-color: {h_color};'>", unsafe_allow_html=True)
            st.markdown(f"<p class='big-font' style='color: {h_color};'>{score}%</p>", unsafe_allow_html=True) [cite: 17]
            st.markdown(f"<h1 style='color: {h_color};'>{level.upper()} RISK</h1>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Profile Details [cite: 18, 19]
            st.subheader("📋 Employee Profile Details")
            c1, c2, c3 = st.columns(3)
            with c1:
                st.write(f"**Grade:** {row.get('GRADE', 'N/A')}")
                st.write(f"**EMPID:** {row.get('EMPID', 'N/A')}")
            with c2:
                st.write(f"**Age:** {row.get('AGE', 'N/A')}")
                st.write(f"**Tenure:** {row.get('TENURE_YRS', 'N/A')} Years")
            with c3:
                st.write(f"**Home:** {row.get('Home State', 'N/A')}")
                st.write(f"**Work:** {row.get('Work City', 'N/A')}")

            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown("<div class='report-card'><h4>🔍 Risk Factor Analysis</h4>", unsafe_allow_html=True)
                if level == 'High':
                    st.write("• Profile falls within Critical Attrition Window (3-5 years) [cite: 21]")
                    st.write("• Distance/Tenure ratio suggests immediate risk [cite: 21]")
                elif level == 'Medium':
                    st.write("• Mid-tenure engagement dip detected [cite: 22]")
                st.markdown("</div>", unsafe_allow_html=True)
            with col_b:
                st.markdown(f"<div class='report-card' style='border-left-color: {h_color};'><h4>🚀 Mitigation Actionables</h4>", unsafe_allow_html=True)
                if level == 'High':
                    st.write("• **ER Physical Intervention:** Urgent 1:1 visit [cite: 24]")
                    st.write("• **Relationship Reset:** Mentorship pairing [cite: 24]")
                elif level == 'Medium':
                    st.write("• **Structured Connect:** ER Manager confidential 1:1 [cite: 25]")
                st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.error("EMPID not found.")

# --- PAGE 3: ER LOGIN ---
elif st.session_state['current_page'] == "ER Login":
    st.title("👤 ER Manager Portal")
    st.markdown("#### Dedicated Dashboard for Mapped Employee Oversight")
    
    er_id = st.number_input("Enter ER Manager ID to Access", min_value=0, step=1)
    
    if er_id:
        # Check if column exists, else use standard fallback
        er_col = 'ER manager ID' if 'ER manager ID' in df.columns else None
        
        if er_col and er_id in df[er_col].values:
            manager_df = df[df[er_col] == er_id]
            high_risk_df = manager_df[manager_df['Risk_Level'] == 'High']
            
            st.divider()
            st.subheader(f"Summary for Manager ID: {er_id}")
            st.metric("Total High Risk Employees Mapped", len(high_risk_df))
            
            if st.button("🔍 View High Risk Employee List"):
                st.session_state['show_er_list'] = True
            
            if st.session_state.get('show_er_list'):
                if not high_risk_df.empty:
                    st.markdown("---")
                    for _, row in high_risk_df.iterrows():
                        with st.container():
                            col1, col2, col3 = st.columns([1, 1, 1])
                            col1.write(f"**ID:** {row['EMPID']}")
                            col2.write(f"**Risk:** {row['Attrition_Risk_Percentage']}%")
                            if col3.button("Analyze details", key=f"btn_{row['EMPID']}"):
                                st.session_state['selected_empid'] = row['EMPID']
                                st.session_state['current_page'] = "Employee risk indicator"
                                st.rerun()
                else:
                    st.success("No high-risk employees found for this Manager ID.")
        else:
            st.error("Manager ID not found in the database.")
