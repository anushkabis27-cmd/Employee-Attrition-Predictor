import streamlit as st
import pandas as pd
import plotly.express as px

# ICICI Branding
ICICI_ORANGE = "#E77817"
ICICI_NAVY = "#05325C"

# --- PAGE 1: ZONE-WISE RISK SUMMARY (QUADRANTS) ---
if st.session_state.page == 'Overview':
    st.title("Zone-wise Risk Summary")
    
    # Data Preparation
    active_df = df[df['Status'] == 'Active']
    high_risk_active = active_df[df['Risk_Level'] == 'High']
    
    # Create the Quadrant Grid (2 Rows, 2 Columns)
    row1_col1, row1_col2 = st.columns(2)
    row2_col1, row2_col2 = st.columns(2)
    
    quadrants = [
        {"zone": "North", "col": row1_col1},
        {"zone": "South", "col": row1_col2},
        {"zone": "East", "col": row2_col1},
        {"zone": "West", "col": row2_col2}
    ]
    
    for quad in quadrants:
        zone = quad["zone"]
        with quad["col"]:
            # 1. Zonal Metrics
            z_total = len(active_df[active_df['ZONE'] == zone])
            z_high_risk = len(high_risk_active[high_risk_active['ZONE'] == zone])
            z_pct = (z_high_risk / z_total * 100) if z_total > 0 else 0
            
            # Display Metric inside the quadrant
            st.subheader(zone)
            st.metric(label="High Risk Count", value=z_high_risk, delta=f"{z_pct:.1f}% Risk Rate", delta_color="inverse")
            
            # 2. Thin Bar Chart with Percentages
            z_dept_data = high_risk_active[high_risk_active['ZONE'] == zone]
            dept_summary = z_dept_data.groupby('MAIN_GROUP').size().reset_index(name='Count')
            
            # Calculate % share of high risk within the zone for the chart tooltip
            dept_summary['Percentage'] = (dept_summary['Count'] / z_high_risk * 100).round(1)
            
            fig = px.bar(
                dept_summary, 
                x='MAIN_GROUP', 
                y='Count',
                text='Percentage', # Shows percentage on top/inside bar
                hover_data={'Percentage': ':.1f%'}, # Interaction shows % on click/hover
                color_discrete_sequence=[ICICI_ORANGE]
            )
            
            # Styling for "Thin" bars and readable layout
            fig.update_traces(width=0.4, texttemplate='%{text}%', textposition='outside')
            fig.update_layout(
                height=300, 
                margin=dict(l=20, r=20, t=30, b=20),
                xaxis_title="", 
                yaxis_title="Count",
                plot_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig, use_container_width=True)
            st.divider()
