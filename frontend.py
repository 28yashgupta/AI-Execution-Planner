import streamlit as st
import requests

# Flask API endpoint
API_URL = "http://127.0.0.1:8080/generate_workflow"

# Streamlit UI
st.title("AI-Powered Workflow Generator 🚀")
st.write("Enter a technical query, and the AI will generate execution steps and code.")

# User input
user_query = st.text_area("Enter your query:", "")

if st.button("Generate Workflow"):
    if user_query.strip():
        # Send request to Flask backend
        response = requests.post(API_URL, json={"query": user_query})
        
        if response.status_code == 200:
            data = response.json()
            
            if "intent" in data:
                st.subheader(f"🧠 Extracted Intent: `{data['intent']}`")
                st.subheader("📌 Execution Steps:")
                for idx, step in enumerate(data["steps"], 1):
                    st.write(f"{idx}. {step}")
                
                st.subheader("📝 Generated Code:")
                st.code(data["code"], language="python")
            else:
                st.warning(data.get("message", "No workflow found. Try another query."))
        else:
            st.error("Error fetching response from the server.")
    else:
        st.warning("Please enter a query.")

