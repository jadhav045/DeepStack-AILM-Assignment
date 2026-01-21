import streamlit as st
import json
from validate_user import validate_user_profile

# 1. Configure the Page
st.set_page_config(
    page_title="AI User Validator",
    page_icon="🤖",
    layout="centered"
)

# 2. Application Title & Description
st.title("🤖 AI User Profile Validator")
st.markdown("""
This tool uses an **LLM (Large Language Model)** to validate user data against strict strict international standards 
(ISO-3166, E.164, etc.) without hardcoded rules.
""")

st.divider()

# 3. The Input Form
with st.form("validation_form"):
    st.subheader("User Profile Input")
    
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("Full Name", placeholder="e.g. Aarav Patel")
        age = st.number_input("Age", min_value=0, max_value=120, value=25)
        country = st.text_input("Country Code", placeholder="e.g. US, IN, FR")
        
    with col2:
        email = st.text_input("Email Address", placeholder="e.g. user@example.com")
        phone = st.text_input("Phone Number", placeholder="e.g. +919876543210")

    # Form Submit Button
    submitted = st.form_submit_button("Validate Profile")

# 4. Logic & Display
if submitted:
    # Construct the JSON object just like the CLI would
    user_data = {
        "name": name,
        "email": email,
        "age": age,
        "country": country,
        "phone": phone
    }

    # Show a spinner while the LLM thinks
    with st.spinner("🤖 Consulting the AI Validator..."):
        result = validate_user_profile(user_data)

    # 5. Display Results
    st.divider()
    st.subheader("Validation Result")

    # Visual Feedback
    if result.get("is_valid"):
        st.success("✅ Profile is Valid")
    else:
        st.error("❌ Profile is Invalid")

    # Metrics Columns
    m1, m2, m3 = st.columns(3)
    m1.metric("Status", "Valid" if result["is_valid"] else "Invalid")
    m2.metric("Errors", len(result["errors"]))
    m3.metric("Warnings", len(result["warnings"]))

    # Display strict JSON output
    st.caption("Raw JSON Output:")
    st.json(result)