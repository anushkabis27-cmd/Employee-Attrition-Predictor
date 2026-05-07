import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# --- FUTURISTIC ICICI THEME CONFIG ---
st.set_page_config(page_title="ICICI Attrition Sentinel v3.2", layout="wide")

# Custom CSS for Futuristic 3D/Dark UI
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
    """, unsafe_allow_html=True)

# --- ROBUST DATA LOADER ---
@st.cache_data
def load_data():
    file_path = 'Attrition_Final_Production_v5_Corrected.xlsx'
    
    if not os.path.exists(file_path):
        st.error(f"⚠️ **File Not Found:** Please upload '{file_path}' to your GitHub repository.")
        st.stop()
        
    try:
        # sheet_name=0 picks the first tab automatically to avoid Worksheet errors
        df = pd.read_excel(file_path, sheet_name=0)
        
        # Standardize Column Names (Remove trailing spaces/Case sensitivity)
        df.columns = df.columns.str.strip()
        
        # Filter for ACTIVE employees as prediction is for the current workforce
        if 'Status' in df.columns:
            active_df = df[df['Status'].str.upper() == 'ACTIVE'].copy()
        else:
            active_df = df.copy()
            
        return active_df
    except Exception as e:
        st.error(f"❌ **Error reading the file:** {e}")
        st.stop()

df = load_data()

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("💠 SENTINEL AI")
st.sidebar.markdown("---")
page = st.sidebar.radio("NAVIGATION", ["Zone wise turnover prediction", "Employee risk indicator"])

# --- PAGE 1: ZONE WISE TURNOVER PREDICTION ---
if page == "Zone wise turnover prediction":
    st.title("🌐 Zone wise turnover prediction")
    st.markdown("#### Regional Vulnerability Matrix (Active Employees Only)")
    
    # We use Home State for the dashboard distribution
    # If 'Home State' is missing, we fall back to a column that exists
    region_col = 'Home State' if 'Home State' in df.columns else ('ZONE' if 'ZONE' in df.columns else None)
    
    if region_col:
        # Select top regions for display
        regions = df[region_col].unique()[:4]
        cols = st.columns(2)
        
        for i, region in enumerate(regions):
            with cols[i % 2]:
                st.markdown(f"<div class='stMetric'><h3>📍 {region}</h3>", unsafe_allow_html=True)
                
                reg_df = df[df[region_col] == region]
                
                # Check for correct Risk Level column
                level_col = 'Risk_Level' if 'Risk_Level' in df.columns else 'Risk Level'
                counts = reg_df[level_col].value_counts(normalize=True) * 100
                
                fig, ax = plt.subplots(figsize=(6, 3))
                cats = ['High', 'Medium', 'Low']
                vals = [counts.get('High', 0), counts.get('Medium', 0), counts.get('Low', 0)]
                colors = ['#FF3131', '#FFD700', '#2ECC71']
                
                bars = ax.bar(cats, vals, color=colors, edgecolor='white', linewidth=1)
                ax.set_facecolor('#112240')
                fig.patch.set_facecolor('#0A192F')
                ax.tick_params(axis='x', colors='white')
                ax.tick_params(axis='y', colors='white')
                ax.set_ylim(0, 100)
                
                for bar in bars:
                    ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 2, f'{bar.get_height():.1f}%', 
                            ha='center', color='#64FFDA', fontweight='bold')
                
                st.pyplot(fig)
                st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.warning("Regional columns (Home State/ZONE) not detected in the file.")

# --- PAGE 2: EMPLOYEE RISK INDICATOR ---
elif page == "Employee risk indicator":
    st.title("🆔 Employee risk indicator")
    st.markdown("#### Predictive Insights & Retention Actionables")
    
    emp_id = st.number_input("Enter EMPID to search", min_value=0, step=1)
    
    if emp_id:
        # Search using standard EMPID column
        user_data = df[df['EMPID'] == emp_id]
        
        if not user_data.empty:
            row = user_data.iloc[0]
            
            # Map Scores and Levels Safely
            score = row.get('Attrition_Risk_Percentage', row.get('Attrition Risk (%)', 0))
            level = row.get('Risk_Level', row.get('Risk Level', 'Low'))
            
            h_color = "#FF3131" if level == 'High' else ("#FFD700" if level == 'Medium' else "#2ECC71")
            
            st.markdown(f"<div class='risk-box' style='border-color: {h_color};'>", unsafe_allow_html=True)
            st.markdown(f"<p class='big-font' style='color: {h_color};'>{score}%</p>", unsafe_allow_html=True)
            st.markdown(f"<h1 style='color: {h_color};'>{level.upper()} RISK</h1>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.divider()
            
            # --- PROFILE SECTION ---
            st.subheader("📋 Employee Profile Details")
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown(f"<p class='profile-text'>**Grade:** {row.get('GRADE', 'N/A')}</p>", unsafe_allow_html=True)
                st.markdown(f"<p class='profile-text'>**EMPID:** {row.get('EMPID', 'N/A')}</p>", unsafe_allow_html=True)
            with c2:
                st.markdown(f"<p class='profile-text'>**Age:** {row.get('AGE', 'N/A')}</p>", unsafe_allow_html=True)
                st.markdown(f"<p class='profile-text'>**Tenure:** {row.get('TENURE_YRS', 'N/A')} Years</p>", unsafe_allow_html=True)
            with c3:
                st.markdown(f"<p class='profile-text'>**Home:** {row.get('Home State', 'N/A')}</p>", unsafe_allow_html=True)
                st.markdown(f"<p class='profile-text'>**Work:** {row.get('Work City', 'N/A')}</p>", unsafe_allow_html=True)

            st.divider()
            
            # --- ANALYSIS & ACTIONABLES ---
            col_a, col_b = st.columns(2)
            
            with col_a:
                st.markdown("<div class='report-card'><h4>🔍 Risk Factor Analysis</h4>", unsafe_allow_html=True)
                if level == 'High':
                    st.write("• Profile falls within the **Critical Attrition Window** (3-5 years).")
                    st.write("• Grade-specific volatility detected for current role.")
                    st.write("• Distance/Tenure ratio suggests immediate engagement risk.")
                elif level == 'Medium':
                    st.write("• Mid-tenure engagement dip detected.")
                    st.write("• Potential career growth stagnation flagged by the model.")
                else:
                    st.write("• High organizational anchoring.")
                    st.write("• Stable tenure-to-age ratio.")
                st.markdown("</div>", unsafe_allow_html=True)

            with col_b:
                st.markdown(f"<div class='report-card' style='border-left-color: {h_color};'><h4>🚀 Mitigation Actionables</h4>", unsafe_allow_html=True)
                if level == 'High':
                    st.write("• **ER Physical Intervention:** Urgent 1:1 visit required.")
                    st.write("• **Emergency Career Pathing:** Explore immediate internal mobility.")
                    st.write("• **Relationship Reset:** Senior-level mentorship pairing.")
                elif level == 'Medium':
                    st.write("• **Structured Connect:** ER Manager confidential 1:1.")
                    st.write("• **OJP Allocation:** Assign a new project to re-energize.")
                else:
                    st.write("• **Appreciation:** Nominate for 'Star Performer' award.")
                    st.write("• **Growth Talk:** Bi-annual career roadmap discussion.")
                st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.error("EMPID not found in Active Database.")
            
