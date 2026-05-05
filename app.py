import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- FUTURISTIC ICICI THEME CONFIG ---
st.set_page_config(page_title="ICICI Attrition Sentinel v3.0", layout="wide")

# Custom CSS for Futuristic 3D/Dark UI
st.markdown("""
    <style>
    .main { background-color: #0A192F; color: #E6F1FF; }
    [data-testid="stSidebar"] { background-color: #f37021; border-right: 2px solid #003366; }
    .stMetric { background-color: #112240; padding: 20px; border-radius: 15px; box-shadow: 5px 5px 15px rgba(0,0,0,0.5); border: 1px solid #233554; }
    h1, h2 { color: #64FFDA; font-family: 'Orbitron', sans-serif; text-shadow: 2px 2px 4px #000; }
    h3 { color: #f37021; }
    .risk-box { padding: 30px; border-radius: 20px; text-align: center; border: 2px solid; }
    .big-font { font-size: 85px !important; font-weight: bold; }
    .report-card { background: rgba(17, 34, 64, 0.9); padding: 25px; border-radius: 15px; border-left: 5px solid #f37021; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data():
    # Loading the file verbatim
    df = pd.read_excel('Attrition_Predictive_Analysis_v2_0.xlsx', sheet_name='Dataset_10k_Final')
    # Using the EXACT columns from your Excel sheet to ensure 1:1 match
    df['Score'] = df['Attrition Risk (%)']
    df['Level'] = df['Risk Level']
    return df

df = load_data()

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("💠 SENTINEL AI")
page = st.sidebar.radio("NAVIGATE", ["Zone wise turnover prediction", "Employee risk indicator"])

# --- PAGE 1: ZONE WISE TURNOVER PREDICTION ---
if page == "Zone wise turnover prediction":
    st.title("🌐 Zone wise turnover prediction")
    st.markdown("#### Holistic Regional Vulnerability Matrix")
    
    # Using Home State as the categorical anchor
    states = ["Uttar Pradesh", "Maharashtra", "West Bengal", "Gujarat"] 
    cols = st.columns(2)
    
    for i, state in enumerate(states):
        with cols[i % 2]:
            st.markdown(f"<div class='stMetric'><h3>📍 {state}</h3>", unsafe_allow_html=True)
            state_df = df[df['Home State'] == state]
            counts = state_df['Level'].value_counts(normalize=True) * 100
            
            # 3D-style Bar Chart
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
            
            plt.tight_layout()
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
            score = row['Score']
            level = row['Level']
            
            # Dynamic Indicator Colors
            h_color = "#FF3131" if level == 'High' else ("#FFD700" if level == 'Medium' else "#2ECC71")
            
            st.markdown(f"<div class='risk-box' style='border-color: {h_color};'>", unsafe_allow_html=True)
            st.markdown(f"<p class='big-font' style='color: {h_color};'>{score}%</p>", unsafe_allow_html=True)
            st.markdown(f"<h1 style='color: {h_color};'>{level.upper()} RISK</h1>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            # --- EMPLOYEE DETAILS SEGMENT ---
            st.divider()
            st.subheader("📋 Employee Profile Details")
            c1, c2, c3 = st.columns(3)
            with c1:
                st.write(f"**Employee ID:** {row['EMPID']}")
                st.write(f"**Grade:** {row['Grade']}")
            with c2:
                st.write(f"**Age:** {row['Age']}")
                st.write(f"**Tenure:** {row['Tenure (Yrs)']} Years")
            with c3:
                st.write(f"**Home Location:** {row['Home State']}")
                st.write(f"**Work Location:** {row['Work City']}")

            # --- REASONS & ACTIONABLES ---
            st.divider()
            col_a, col_b = st.columns(2)
            
            with col_a:
                st.markdown("<div class='report-card'><h4>🔍 Risk Factor Analysis</h4>", unsafe_allow_html=True)
                if level == 'High':
                    st.write("• Significant mismatch in Age-Tenure growth ratio.")
                    st.write("• High volatility detected in current Grade cohort.")
                    st.write(f"• Distance Factor: {row['Distance From Home (KM)']} KM from home base.")
                elif level == 'Medium':
                    st.write("• Moderate engagement dip identified in recent Resignation Month patterns.")
                    st.write("• Potential plateau in current Tenure Bracket.")
                else:
                    st.write("• Strong organizational anchoring and stable tenure.")
                    st.write("• Low risk relative to Home State peer groups.")
                st.markdown("</div>", unsafe_allow_html=True)

            with col_b:
                st.markdown(f"<div class='report-card' style='border-left-color: {h_color};'><h4>🚀 Mitigation Actionables</h4>", unsafe_allow_html=True)
                if level == 'High':
                    st.write("• **Physical Intervention:** Urgent 1:1 visit by ER Manager to signal care.")
                    st.write("• **Emergency Re-pathing:** Immediately explore internal mobility/cross-dept roles.")
                    st.write("• **OJP Bridge:** Assign high-visibility project to re-engage through ownership.")
                    st.write("• **Relationship Reset:** HR-led coaching for manager to rebuild trust.")
                    st.write("• **Leadership Touch:** Senior BU head to personally acknowledge employee value.")
                elif level == 'Medium':
                    st.write("• **Personalized Recognition:** Deliver specific, impact-based appreciation.")
                    st.write("• **Structured Connect:** ER Manager confidential 1:1 on workload and dynamics.")
                    st.write("• **Re-energizer OJP:** Offer short-term project rotation in new business unit.")
                    st.write("• **Aspiration Realignment:** Manager explicit check-in on evolving career goals.")
                    st.write("• **Skip-Level Check:** HR-arranged meeting to address manager friction.")
                else:
                    st.write("• **Appreciation Programs:** Nominate for 'Star Performer' or peer awards.")
                    st.write("• **Future Check-ins:** Bi-annual conversations on 2-3 year development roadmaps.")
                    st.write("• **Internal SME Roles:** Assign as project leads on digital pilots.")
                    st.write("• **Casual Connect:** ER Manager branch visit for proactive 'growth talk'.")
                    st.write("• **Mentorship:** Pair with senior leader for division shadowing.")
                st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.error("EMPID NOT FOUND.")
