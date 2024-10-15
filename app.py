import streamlit as st
import requests
import json

# Streamlit app title
st.title("AiDentify's Comprehensive Case-Based Learning in Dentistry")

# Instructions
st.write("""
### Welcome to the Case-Based Learning (CBL) platform for dental education!
Here, you can enter patient cases, get AI-based analysis for diagnosis and treatment options.
""")

# API key input from the user
api_key = st.text_input("Enter your OpenAI API Key", type="password")

# Case Input Section
st.subheader("Case Scenario Input")
st.write("Fill in the details of the dental case scenario below:")

# Inputs for case scenario
patient_history = st.text_area("Patient History", "A 45-year-old male with a history of smoking and diabetes.")
symptoms = st.text_area("Symptoms", "Chronic gum bleeding, bad breath, and tooth sensitivity.")
examination = st.text_area("Clinical Examination", "Inflamed gums, periodontal pockets, bone loss in X-rays.")
diagnostic_tests = st.text_area("Diagnostic Tests", "Periodontal probing, radiographs showing bone loss.")
treatment_focus = st.selectbox("Focus of AI Analysis", ["Diagnosis", "Treatment Plan", "Clinical Advice"])

# OpenAI API call function (using v1/chat/completions endpoint)
def get_openai_response(patient_history, symptoms, examination, diagnostic_tests, treatment_focus, api_key):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    messages = [
        {"role": "system", "content": "You are an expert dental clinician."},
        {"role": "user", "content": f"Patient History: {patient_history}"},
        {"role": "user", "content": f"Symptoms: {symptoms}"},
        {"role": "user", "content": f"Clinical Examination: {examination}"},
        {"role": "user", "content": f"Diagnostic Tests: {diagnostic_tests}"},
        {"role": "user", "content": f"Provide a detailed {treatment_focus.lower()} for the case."}
    ]
    
    data = {
        "model": "gpt-3.5-turbo",  # You can change this to gpt-4 if you have access
        "messages": messages,
        "max_tokens": 300,
        "temperature": 0.7
    }
    
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content'].strip()
    else:
        return f"Error: Unable to fetch response. Status code: {response.status_code}. Reason: {response.text}"

# Button to trigger the analysis
if st.button("Get AI Analysis"):
    if api_key:
        with st.spinner('Analyzing case...'):
            response = get_openai_response(patient_history, symptoms, examination, diagnostic_tests, treatment_focus, api_key)
            st.subheader("AI-Generated Case Analysis")
            st.write(response)
    else:
        st.error("Please enter your OpenAI API key.")
