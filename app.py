import streamlit as st
import pandas as pd

# (Previous setup code remains the same: branding colors and data loading)
ICICI_ORANGE = "#E77817"
ICICI_NAVY = "#05325C"
RED = "#FF0000"
YELLOW = "#FFD700"
GREEN = "#008000"

# ... [Data Loading Code for Attrition_Final_Production_v5_Corrected.xlsx] ...

# --- PAGE 2: EMPLOYEE SEARCH ---
if st.session_state.page == 'Search':
    st.markdown(f"<h1 style='color:{ICICI_NAVY};'>Employee Search</h1>", unsafe_allow_html=True)
    
    # Search Bar with Clickable Button
    s_col1, s_col2 = st.columns([4, 1])
    with s_col1:
        search_id = st.text_input("Enter 6-Digit Employee ID:", placeholder="e.g. 924197", label_visibility="collapsed")
    with s_col2:
        search_clicked = st.button("SEARCH DETAILS", use_container_width=True)

    if search_clicked and search_id:
        res = df[df['EMPID'] == search_id.strip()]
        if not res.empty:
            emp = res.iloc[0]
            
            # 1. Color-coded Risk Score (Center Aligned)
            risk_color = RED if emp['Risk_Level'] == 'High' else (YELLOW if emp['Risk_Level'] == 'Medium' else GREEN)
            st.markdown(f"""
                <div style='text-align:center; padding:20px;'>
                    <h1 style='color:{risk_color}; font-size:100px; margin:0;'>{emp['Attrition_Risk_Percentage']}%</h1>
                    <h2 style='color:{risk_color}; margin-top:0;'>{emp['Risk_Level']} Risk</h2>
                </div>
            """, unsafe_allow_html=True)
            
            st.divider()

            # 2. Main Layout Columns
            detail_col, insight_col = st.columns([1, 1.5])

            with detail_col:
                st.markdown(f"<h4 style='color:{ICICI_NAVY};'>Employee Details</h4>", unsafe_allow_html=True)
                st.write(f"**Emp ID:** {emp['EMPID']}")
                st.write(f"**Age:** {emp['AGE']} Years")
                st.write(f"**Grade:** {emp['GRADE']}")
                st.write(f"**Tenure:** {emp['TENURE_YRS']} Years")
                st.write(f"**Work Location:** {emp['ZONE']}")
                st.write(f"**Home Location:** Mumbai (HQ)") # Placeholder for Home Location

            with insight_col:
                # 3. Reasons Box (Upper)
                st.markdown(f"<h4 style='color:{ICICI_NAVY}; text-align:left;'>Reasons</h4>", unsafe_allow_html=True)
                with st.container(border=True):
                    reasons = []
                    if 25 <= emp['AGE'] <= 29: reasons.append("Age falls within the high-risk bracket (25-29 years).")
                    if emp['TENURE_YRS'] > 3: reasons.append(f"Tenure has reached {emp['TENURE_YRS']} years, exceeding the 3-year threshold.")
                    if emp['Dist_Bin'] == 3: reasons.append("Current work location is significantly far from home for over a year.")
                    if emp['Grade_Numeric'] in [4, 5]: reasons.append(f"Positioned in {emp['GRADE']} grade which is a high-attrition segment.")
                    
                    if not reasons: reasons.append("Score driven by standard baseline behavioral indicators.")
                    for r in reasons: st.write(f"• {r}")

                # 4. Actionables Box (Lower)
                st.markdown(f"<h4 style='color:{ICICI_NAVY}; text-align:left;'>Actionables</h4>", unsafe_allow_html=True)
                with st.container(border=True):
                    if emp['Risk_Level'] == 'Low':
                        st.write("• **Aspiration Check-ins**: Conduct bi-annual 'Future Goals' conversations to create 2–3 year roadmaps.")
                        st.write("• **ER Manager Connect**: Casual branch visit to surface silent dissatisfiers and update iCare.")
                        st.write("• **Recognition**: Nominate for peer-recognition awards to reinforce organizational value.")
                    
                    elif emp['Risk_Level'] == 'Medium':
                        st.write("• **Manager Recognition**: Deliver specific, meaningful appreciation for actual impact (e.g., audit handling).")
                        st.write("• **Structured ER Meet**: Conduct confidential 1:1 to address team dynamics and record findings in iCare.")
                        st.write("• **OJP Re-energizer**: Offer a short-term project secondment in a different business unit to reignite motivation.")
                    
                    elif emp['Risk_Level'] == 'High':
                        st.write("• **ER Manager Intervention**: Urgent in-person visit to signal genuine care and de-escalate job searching.")
                        st.write("• **Emergency Career Pathing**: Immediately explore internal mobility options across departments.")
                        st.write("• **Leadership Touch**: BU/HR Head personal acknowledgment to signal visible value to the broad organization.")
        else:
            st.error("Employee ID not found in the database.")
