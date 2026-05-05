import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration & ICICI Branding
st.set_page_config(page_title="ICICI Turnover Predictor", layout="wide")

ICICI_ORANGE = "#E77817"
ICICI_NAVY = "#05325C"

# 2. Data Loading (Updated for the corrected file)
@st.cache_data
def load_data():
    try:
        # Load the newly uploaded corrected file
        # Note: If you renamed it to Attrition_Final_Production_v5_Corrected.xlsx in Colab, use that name here.
        data = pd.read_excel("Attrition_Final_Production_v5_Corrected.xlsx")
        
        # Standardizing formats
        data['EMPID'] = data['EMPID'].astype(str).str.zfill(6)
        return data
    except FileNotFoundError:
        st.error("Dataset not found. Please ensure 'Attrition_Final_Production_v5_Corrected.xlsx' is uploaded to GitHub.")
        st.stop()

df = load_data()

# 3. Navigation State Management
if 'page' not in st.session_state:
    st.session_state.page = 'Overview'

# Toggle Navigation
col_n1, col_n2 = st.columns(2)
with col_n1:
    if st.button("Zone-wise Risk Summary", use_container_width=True):
        st.session_state.page = 'Overview'
with col_n2:
    if st.button("Employee Search", use_container_width=True):
        st.session_state.page = 'Search'

st.divider()

# --- PAGE 1: ZONE-WISE RISK SUMMARY (QUADRANTS) ---
if st.session_state.page == 'Overview':
    st.title("Zone-wise Risk Summary")
    
    active_df = df[df['Status'] == 'Active']
    high_risk_active = active_df[active_df['Risk_Level'] == 'High']
    
    # 2x2 Quadrant Grid
    q_row1 = st.columns(2)
    q_row2 = st.columns(2)
    
    zones = [
        {"name": "North", "col": q_row1[0]},
        {"name": "South", "col": q_row1[1]},
        {"name": "East", "col": q_row2[0]},
        {"name": "West", "col": q_row2[1]}
    ]
    
    for q in zones:
        zone_name = q["name"]
        with q["col"]:
            # Zonal Metrics
            z_active = active_df[active_df['ZONE'] == zone_name]
            z_high = high_risk_active[high_risk_active['ZONE'] == zone_name]
            
            z_count = len(z_high)
            z_rate = (z_count / len(z_active) * 100) if len(z_active) > 0 else 0
            
            st.subheader(zone_name)
            st.metric(label="High Risk Count", value=f"{z_count} Employees", 
                      delta=f"{z_rate:.1f}% Risk Rate", delta_color="inverse")
            
            # Interactive Thin Bar Chart
            dept_summary = z_high.groupby('MAIN_GROUP').size().reset_index(name='Count')
            dept_summary['Percentage'] = (dept_summary['Count'] / z_count * 100).round(1) if z_count > 0 else 0
            
            fig = px.bar(dept_summary, x='MAIN_GROUP', y='Count', 
                         text='Percentage', hover_data={'Percentage': ':.1f%'},
                         color_discrete_sequence=[ICICI_ORANGE])
            
            fig.update_traces(width=0.35, texttemplate='%{text}%', textposition='outside')
            fig.update_layout(height=300, margin=dict(l=10, r=10, t=30, b=10), 
                              xaxis_title="", yaxis_title="Count", plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
            st.divider()

# --- PAGE 2: EMPLOYEE SEARCH ---
elif st.session_state.page == 'Search':
    st.title("Individual Risk Predictor")
    search_id = st.text_input("Enter 6-Digit EMPID:", key="search_box")
    
    if search_id:
        result = df[df['EMPID'] == search_id.strip()]
        if not result.empty:
            emp = result.iloc[0]
            if emp['Status'] == 'Inactive':
                st.warning("Note: This employee record indicates they have already left.")
            else:
                # Main Risk Output
                st.markdown(f"<h1 style='text-align:center; color:{ICICI_ORANGE}; font-size:100px;'>{emp['Attrition_Risk_Percentage']}%</h1>", unsafe_allow_html=True)
                st.markdown(f"<h2 style='text-align:center;'>{emp['Risk_Level']} ATTRITION RISK</h2>", unsafe_allow_html=True)
                
                # Details Table
                st.divider()
                cols = st.columns(4)
                cols[0].write(f"**Grade:** {emp['GRADE']}")
                cols[1].write(f"**Tenure:** {emp['TENURE_YRS']} Yrs")
                cols[2].write(f"**Age:** {emp['AGE']}")
                cols[3].write(f"**Zone:** {emp['ZONE']}")
                
                # Actionables
                st.subheader("Model-Driven Recommendations")
                st.write(f"- **Risk Window**: Employee is in the critical **{emp['TENURE_YRS']} year** tenure bracket.")
                st.write(f"- **Engagement**: Schedule a priority stay interview before the upcoming seasonal peak.")
                if emp['Dist_Bin'] == 3:
                    st.write("- **Logistics**: Discuss relocation or work-from-home options to mitigate 'Outstation' distance stress.")
        else:
            st.error("EMPID not found in active records.")
