# --- PAGE 2: EMPLOYEE RISK INDICATOR ---
elif page == "Employee risk indicator":
    st.title("👤 Employee Risk Indicator")
    st.markdown("<h3 style='color: #f37021;'>Predictive Attrition Individual Search</h3>", unsafe_allow_html=True)
    
    emp_id = st.number_input("Enter Employee ID", min_value=0, step=1)
    
    if emp_id:
        user_data = df[df['EMPID'] == emp_id]
        
        if not user_data.empty:
            score = user_data['Risk_Score'].values[0]
            
            # FIXED LOGIC: Correcting the variable assignments
            if score >= 75:
                status = "HIGH RISK"
                hex_color = "#FF0000" # Red
            elif score >= 40:
                status = "MEDIUM RISK"
                hex_color = "#FFCC00" # Yellow
            else:
                status = "LOW RISK"
                hex_color = "#008000" # Green
            
            # Display Score & Indicator
            st.markdown(f"<p class='big-font' style='color: {hex_color};'>{score}%</p>", unsafe_allow_html=True)
            st.markdown(f"<h2 style='text-align: center; color: {hex_color};'>{status}</h2>", unsafe_allow_html=True)
            
            st.divider()
            
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("💡 Analysis Factors")
                st.write(f"**Tenure:** {user_data['TENURE_YRS'].values[0]} Years")
                st.write(f"**Grade:** {user_data['GRADE'].values[0]}")
                st.write(f"**Age:** {user_data['AGE'].values[0]}")
                st.write("* Model identifies specific volatility based on historical lateral movement trends.")

            with col2:
                st.subheader("🚀 Actionables")
                if status == "HIGH RISK":
                    st.write("* **ER manager should contact and understand career aspirations.**")
                    st.write("* **Evaluate for retention bonus or immediate role enrichment.**")
                elif status == "MEDIUM RISK":
                    st.write("* **Schedule skip-level meeting to discuss growth path.**")
                    st.write("* **Enroll in specialized leadership or skill-building modules.**")
                else:
                    st.write("* **Continue standard performance tracking.**")
                    st.write("* **Nominate for internal reward and recognition programs.**")
        else:
            st.error("Employee ID not found in database.")
