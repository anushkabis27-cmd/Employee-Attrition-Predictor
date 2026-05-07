import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- FUTURISTIC ICICI THEME CONFIG ---
st.set_page_config(page_title="ICICI Attrition Sentinel v3.1", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0A192F; color: #E6F1FF; }
    [data-testid="stSidebar"] { background-color: #f37021; }
    .stMetric { background-color: #112240; padding: 20px; border-radius: 15px; border: 1px solid #233554; }
    h1, h2 { color: #64FFDA; font-family: 'Arial'; text-shadow: 2px 2px 4px #000; }
    .risk-box { padding: 30px; border-radius: 20px; text-align: center; border: 2px solid; background: rgba(0,0,0,0.3); }
    .big-font { font-size: 85px !important; font-weight: bold; }
    .report-card { background: rgba(17, 34, 64, 0.9); padding: 25px; border-radius: 15px; border-left: 5px solid #f37021; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data():
    # Loading the corrected file verbatim
    file_path = 'Attrition_Predictive_Model_v5_Corrected.xlsx'
    df = pd.read_excel(file_path, sheet_name='Dataset_10k_Final')
    
    # Filter for ACTIVE employees only
    active_df = df[df['Status'].str.upper() == 'ACTIVE'].copy()
    return active_df

df = load_data()

# --- SIDEBAR ---
st.sidebar.title("💠 SENTINEL AI v3.1")
page = st.sidebar.radio("NAVIGATE", ["Zone wise turnover prediction", "Employee risk indicator"])

# --- PAGE 1: ZONE WISE TURNOVER PREDICTION ---
if page == "Zone wise turnover prediction":
    st.title("🌐 Zone wise turnover prediction")
    st.markdown("#### Regional Vulnerability Matrix (Corrected SO Tenure Data)")
    
    # Using specific sample states from the dataset for visualization
    states = ["Uttar Pradesh", "Maharashtra", "West Bengal", "Gujarat"] 
    cols = st.columns(2)
    
    for i, state in enumerate(states):
        # Fallback if Home State column name varies in the Excel
        state_col = 'Home State' if 'Home State' in df.columns else 'GRADE' # Proxy for demo if col missing
        
        with cols[i % 2]:
            st.markdown(f"<div class='stMetric'><h3>📍 {state if state_col == 'Home State' else 'Grade: ' + state}</h3>", unsafe_allow_html=True)
            
            # Filtering and calculating percentages
            state_df = df[df[state_col] == state] if state_col in df.columns else df.head(100)
            counts = state_df['Risk_Level'].value_counts(normalize=True) * 100
            
            fig, ax = plt.subplots(figsize=(6, 3))
            cats = ['High', 'Medium', 'Low']
            vals = [counts.get('High', 0), counts.get('Medium', 0), counts.get('Low', 0)]
            colors = ['#FF3131', '#FFD700', '#2ECC71']
            
            bars = ax.bar(cats, vals, color=colors, edgecolor='white')
            ax.set_facecolor('#112240')
            fig.patch.set_facecolor('#0A192F')
            ax.tick_params(colors='white')
            ax.set_ylim(0, 100)
            
            for bar in bars:
                ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 2, f'{bar.get_height():.1f}%', 
                        ha='center', color='#64FFDA', fontweight='bold')
            
            st.pyplot(fig)
            st.markdown("</div>", unsafe_allow_html=True)

# --- PAGE 2: EMPLOYEE RISK INDICATOR ---
elif page == "Employee risk indicator":
    st.title("🆔 Employee risk indicator")
    emp_id = st.number_input("Enter EMPID", min_value=0, step=1)
    
    if emp_id:
        user_data = df[df['EMPID'] == emp_id]
        if not user_data.empty:
            row = user_data.iloc[0]
            score, level = row['Attrition_Risk_Percentage'], row['Risk_Level']
            h_color = "#FF3131" if level == 'High' else ("#FFD700" if level == 'Medium' else "#2ECC71")
            
            st.markdown(f"<div class='risk-box' style='border-color: {h_color};'>", unsafe_allow_html=True)
            st.markdown(f"<p class='big-font' style='color: {h_color};'>{score}%</p>", unsafe_allow_html=True)
            st.markdown(f"<h1 style='color: {h_color};'>{level.upper()} RISK</h1>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.divider()
            st.subheader("📋 Profile Details")
            c1, c2, c3 = st.columns(3)
            with c1:
                st.write(f"**Grade:** {row['GRADE']}")
                st.write(f"**Status:** {row['Status']}")
            with c2:
                st.write(f"**Age:** {row['AGE']}")
                st.write(f"**Tenure:** {row['TENURE_YRS']} Years")
            with c3:
                st.write(f"**Work City:** {row['Resignation_Month_Name'] if 'Resignation_Month_Name' in df.columns else 'N/A'}")
                st.write(f"**Distance:** {row['Distance_From_Home_KM']} KM")

            st.divider()
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown("<div class='report-card'><h4>🔍 Risk Factor Analysis</h4>", unsafe_allow_html=True)
                if level == 'High':
                    st.write("• **Critical Cohort:** Profile matches 3-5yr tenure & DM/M grade volatility.")
                elif level == 'Medium':
                    st.write("• **Engagement Plateau:** Employee entering a mid-tenure risk bracket.")
                else:
                    st.write("• **Stability Anchor:** Profile falls outside the primary vulnerable segments.")
                st.markdown("</div>", unsafe_allow_html=True)

            with col_b:
                st.markdown(f"<div class='report-card' style='border-left-color: {h_color};'><h4>🚀 Mitigation Actionables</h4>", unsafe_allow_html=True)
                if level == 'High':
                    st.write("• **Physical Intervention:** Urgent 1:1 visit by ER Manager.")
                    st.write("• **Internal Mobility:** Explore immediate cross-functional paths.")
                elif level == 'Medium':
                    st.write("• **Structured Connect:** Scheduled check-in on workload/manager relationship.")
                else:
                    st.write("• **Star Recognition:** Nominate for quarterly appreciation.")
                st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.error("EMPID NOT FOUND (Only Active employees are processed).")
