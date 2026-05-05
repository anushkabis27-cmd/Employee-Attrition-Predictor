import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration & ICICI Branding
st.set_page_config(page_title="ICICI Turnover Predictor", layout="wide")

# Brand Color Palette
ICICI_ORANGE = "#E77817"
ICICI_NAVY = "#05325C"
BACKGROUND_WHITE = "#FFFFFF"

# Custom CSS for UI Design
st.markdown(f"""
    <style>
    .main {{ background-color: {BACKGROUND_WHITE}; }}
    h1, h2, h3 {{ color: {ICICI_NAVY}; font-family: 'Arial'; }}
    .stMetric {{ 
        background-color: #F8F9FA; 
        padding: 20px; 
        border-radius: 10px; 
        border-top: 5px solid {ICICI_ORANGE}; 
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }}
    /* Top Toggle Navigation Style */
    .nav-container {{
        display: flex;
        justify-content: center;
        gap: 50px;
        margin-bottom: 20px;
    }}
    .nav-link {{
        font-size: 20px;
        font-weight: bold;
        text-decoration: none;
        color: {ICICI_NAVY};
        border-bottom: 3px solid transparent;
        transition: 0.3s;
    }}
    .nav-link:hover {{ border-bottom: 3px solid {ICICI_ORANGE}; }}
    </style>
""", unsafe_allow_html=True)

# 2. Load Processed Data
@st.cache_data
def load_data():
    # Use the file generated in Colab with ZONE and MAIN_GROUP
    return pd.read_excel("Attrition_Final_Production.xlsx")

df = load_data()

# 3. Top-Level Toggle Navigation (State Management)
if 'page' not in st.session_state:
    st.session_state.page = 'Overview'

col1, col2 = st.columns([1,1])
with col1:
    if st.button("Zonal Overview Dashboard", use_container_width=True):
        st.session_state.page = 'Overview'
with col2:
    if st.button("Individual Employee Search", use_container_width=True):
        st.session_state.page = 'Search'

st.divider()

# --- PAGE 1: ZONAL OVERVIEW ---
if st.session_state.page == 'Overview':
    st.title("Organizational Risk Summary")
    
    # Filter for Active High Risk only
    active_high_risk = df[(df['Status'] == 'Active') & (df['Risk_Level'] == 'High')]
    
    # 4 Separate Zonal Boxes
    zones = ['North', 'South', 'East', 'West']
    z_cols = st.columns(4)
    for i, zone in enumerate(zones):
        count = len(active_high_risk[active_high_risk['ZONE'] == zone])
        z_cols[i].metric(label=f"{zone} Zone", value=count, delta="Active High Risk")

    st.write("### Department-wise Risk Concentration")
    
    # Bar Charts in 2x2 Grid
    chart_rows = st.columns(2)
    for i, zone in enumerate(zones):
        with chart_rows[i % 2]:
            z_data = active_high_risk[active_high_risk['ZONE'] == zone]
            dept_counts = z_data.groupby('MAIN_GROUP').size().reset_index(name='Count')
            
            fig = px.bar(dept_counts, x='MAIN_GROUP', y='Count', 
                         title=f"{zone} Zone: High Risk by Department",
                         color_discrete_sequence=[ICICI_ORANGE],
                         labels={'MAIN_GROUP': 'Department', 'Count': 'High Risk Count'})
            fig.update_layout(plot_bgcolor='white')
            st.plotly_chart(fig, use_container_width=True)

# --- PAGE 2: EMPLOYEE SEARCH ---
elif st.session_state.page == 'Search':
    st.title("Employee Attrition Predictor")
    
    search_id = st.text_input("Search by 6-Digit Employee ID:", placeholder="Enter EMPID...")
    
    if search_id:
        # Search the 12,000 record database
        result = df[df['EMPID'].astype(str) == search_id.strip()]
        
        if not result.empty:
            emp = result.iloc[0]
            
            if emp['Status'] == 'Inactive':
                st.error(f"Employee {search_id} has already exited the organization.")
            else:
                # Main Risk Output (Large Font)
                st.markdown(f"<p style='text-align:center; font-size:100px; color:{ICICI_ORANGE}; font-weight:bold; margin-bottom:0;'>{emp['Attrition_Risk_Percentage']}%</p>", unsafe_allow_html=True)
                st.markdown(f"<h2 style='text-align:center; color:{ICICI_NAVY}; margin-top:0;'>{emp['Risk_Level']} RISK LEVEL</h2>", unsafe_allow_html=True)
                
                st.divider()
                
                # Employee Details below
                d1, d2, d3, d4 = st.columns(4)
                d1.write(f"**Grade:** {emp['GRADE']}")
                d2.write(f"**Tenure:** {emp['TENURE_YRS']} Years")
                d3.write(f"**Age:** {emp['AGE']}")
                d4.write(f"**Current Zone:** {emp['ZONE']}")
                
                # Insights and Actionables in Bullet Points
                st.divider()
                col_i, col_a = st.columns(2)
                with col_i:
                    st.subheader("Model Insights")
                    st.write(f"* Falls in the critical **{emp['Tenure_Bracket']}** tenure bracket.")
                    st.write(f"* Assigned to high-risk grade **{emp['GRADE']}**.")
                    if emp['Age_Tenure_Factor'] > 100:
                        st.write("* Age-Tenure interaction indicates high lateral marketability.")
                
                with col_a:
                    st.subheader("Actionable Steps")
                    st.write("* **Retention Conversation**: Conduct a 1-on-1 before the June/July cycle.")
                    st.write(f"* **Career Pathing**: Discuss progression for the next {emp['GRADE']} promotion.")
                    if emp['Dist_Bin'] == 3:
                        st.write("* **Relocation Support**: Address potential stress for 'Outstation' status (>200km).")
        else:
            st.warning("No active employee found with that ID.")
   
