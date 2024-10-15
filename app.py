import streamlit as st
import requests
import json

# Streamlit app title
st.title("Comprehensive Case-Based Learning in Dentistry")

# Instructions
st.write("""
### Welcome to the Case-Based Learning (CBL) platform for dental education!
Here, you can enter patient cases, get AI-based analysis for diagnosis and treatment options, and reflect on your learning.
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

# OpenAI API call function
def get_openai_response(prompt, api_key):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "text-davinci-003",
        "prompt": prompt,
        "max_tokens": 300,
        "n": 1,
        "stop": None,
        "temperature": 0.7
    }
    
    response = requests.post("https://api.openai.com/v1/completions", headers=headers, data=json.dumps(data))
    
    if response.status_code == 200:
        return response.json()['choices'][0]['text'].strip()
    else:
        return "Error: Unable to fetch response. Please check your API key or input."

# Constructing the prompt for OpenAI based on the user inputs
def construct_prompt(patient_history, symptoms, examination, diagnostic_tests, treatment_focus):
    return f"""
    You are an expert dental clinician. Analyze the following case and provide a detailed {treatment_focus.lower()}.

    Patient History: {patient_history}
    Symptoms: {symptoms}
    Clinical Examination: {examination}
    Diagnostic Tests: {diagnostic_tests}

    Based on the above details, provide a comprehensive {treatment_focus.lower()} for the patient.
    """

# Reflection and feedback section
st.subheader("Reflection and Feedback")
reflection_prompt = st.text_area("Reflect on the case and your learning", "What were the key considerations in this case? How did you approach the diagnosis or treatment?")
feedback_prompt = st.text_area("Provide feedback on the analysis", "Was the AI's analysis helpful? Did it match your own expectations?")

# Button to trigger the analysis
if st.button("Get AI Analysis"):
    if api_key:
        with st.spinner('Analyzing case...'):
            prompt = construct_prompt(patient_history, symptoms, examination, diagnostic_tests, treatment_focus)
            response = get_openai_response(prompt, api_key)
            st.subheader("AI-Generated Case Analysis")
            st.write(response)
    else:
        st.error("Please enter your OpenAI API key.")

# Button for reflection submission
if st.button("Submit Reflection"):
    st.success("Thank you for your reflection and feedback!")
