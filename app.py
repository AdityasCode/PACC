import os

import dotenv
import streamlit as st
import streamlit_analytics
from openai import OpenAI

# Load environment variables
dotenv.load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)
print(OPENAI_API_KEY)

# Setup streamlit
streamlit_analytics.start_tracking()

# Function to get GPT output
system_msg = {
    "role": "system",
    "content": (
        "You are an AI assistant integrated into a climate change prediction app. Your purpose is to provide concise, "
        "to-the-point responses regarding the ecological impact of climate change, its effects on medical conditions, "
        "job market implications, and advice on relocation or lifestyle modifications based on user input. I will give "
        "you information about this user in pieces."
    )
}
messages_array = [system_msg]


def get_gpt_output(prompt):
    messages_array.append({"role": "user", "content": prompt})
    raw_response = client.chat.completions.create(model="gpt-3.5-turbo",
                                                  messages=messages_array,
                                              temperature=0)
    response = raw_response.choices[0].message.content
    messages_array.append({"role": "assistant", "content": response})
    return response


# Set page configuration
st.set_page_config(
    page_title="Climate Change Impact Predictions",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Title and description
st.title("🌍 Climate Change Impact Predictions 🌿 v2")
st.write("""
Welcome to the Climate Change Impact Prediction app. This tool helps you understand how climate change might affect various aspects of your life based on your demographics and current situation.
""")

# Collecting user inputs
st.header("Input your information")

# Location
location = st.text_input("Your location (City):", placeholder="Enter your city")

# Age
age = st.number_input("Your age:", min_value=0, max_value=120, step=1)

# Medical conditions
medical_conditions = st.text_area("List your medical conditions:",
                                  placeholder="Enter your medical conditions, separated by commas")

# Finances
st.subheader("Your Finances")
net_worth = st.number_input("Current net worth ($):", min_value=0, step=1000)
asset_worth = st.number_input("Asset worth ($):", min_value=0, step=1000)

# Job
job = st.text_input("Your job title:", placeholder="Enter your job title")

# Confidence in getting another job
job_confidence = st.slider("Confidence in getting another job (1-100):", min_value=1, max_value=100, step=1)

# Years into the future
years_future = st.slider("How many years into the future do you want to predict?", min_value=1, max_value=50, value=10)

# Error checking
errors = []

if st.button("Submit"):
    if not location:
        errors.append("Location is required.")
    if age == 0:
        errors.append("Age must be greater than 0.")
    if not medical_conditions:
        errors.append("Medical conditions are required.")
    if net_worth == 0:
        errors.append("Net worth must be greater than 0.")
    if asset_worth == 0:
        errors.append("Asset worth must be greater than 0.")
    if not job:
        errors.append("Job title is required.")

    if errors:
        st.error("\n".join(errors))
    else:
        # Display loading message
        st.spinner('Calculating predictions... Please wait...')

        # Generate output using GPT
        ecological_prompt = str(
            f"Describe the ecological impact on {location} in {years_future.f} years due to climate change.")
        ecological_impact = get_gpt_output(ecological_prompt)

        medical_prompt = str(
            f"Describe how {medical_conditions} in {location} might be impacted by climate change in {years_future} years.")
        medical_impact = get_gpt_output(medical_prompt)

        job_prompt = str(
            f"Describe how a {job} might be impacted by climate change in {years_future} years.")
        job_impact = get_gpt_output(job_prompt)

        relocation_prompt = str(
            f"Recommend whether a person with ${net_worth} in bank account and ${asset_worth} in assets should relocate"
            f" due to climate change in {years_future} years, and suggest nearby locations.")
        relocation_recommendation = get_gpt_output(relocation_prompt)

        modification_prompt = str(
            f"Suggest modifications for living space, daily lifestyle, or diet to prepare for climate change effects in"
            f" {years_future} years.")
        modifications = get_gpt_output(modification_prompt)

        # Display results
        st.header("Predictions")

        st.subheader(str(f"Ecological Impact on {location} in {years_future} years"))
        st.write(ecological_impact)

        st.subheader(str(f"Impact on Medical Conditions in {years_future} years"))
        st.write(medical_impact)

        st.subheader(str(f"Impact on Job in {years_future} years"))
        st.write(job_impact)

        st.subheader("Relocation Recommendation")
        st.write(relocation_recommendation)

        st.subheader("Modifying Your Living Space, Daily Lifestyle, or Diet")
        st.write(modifications)

        # Selectbox for FAQs
faq_options = {
    "What does the app do with my location?": """
    The app uses your location to provide region-specific climate change impact predictions. This includes ecological changes, potential health risks, and job market shifts that might affect your area.
    """,
    "Why do you need my age?": """
    Your age helps us tailor the predictions to your stage of life. Different age groups may experience the impacts of climate change differently, especially in terms of health and job market implications.
    """,
    "How are my medical conditions relevant?": """
    Climate change can exacerbate certain medical conditions. By knowing your medical history, the app can provide more accurate predictions on how climate change might impact your health and offer personalized recommendations.
    """,
    "What do you do with my financial information?": """
    Your financial information, including net worth and asset worth, helps the app assess your ability to relocate or adapt to climate change. This information is used to give you tailored advice on whether moving is a viable option or if you should modify your living space and lifestyle.
    """,
    "Why is my job and confidence in getting another job important?": """
    Your job and your confidence in securing another job are crucial in understanding your economic stability. Climate change can impact job markets, and this information helps us predict how your employment might be affected and provide recommendations accordingly.
    """,
    "How does the app use the 'years into the future' slider?": """
    The 'years into the future' slider allows you to choose a time frame for the predictions. The app adjusts its predictions based on the selected number of years, offering a forward-looking view of the potential impacts of climate change.
    """,
    "What do the ecological impact predictions mean?": """
    Ecological impact predictions describe how your city might be affected by climate change. This includes changes in weather patterns, sea level rise, and other environmental factors that could impact daily life and infrastructure.
    """,
    "How does climate change affect my medical conditions?": """
    Certain medical conditions can worsen due to climate change. For example, increased air pollution and higher temperatures can exacerbate respiratory conditions like asthma. The app provides insights into how your specific medical conditions might be impacted.
    """,
    "How can climate change impact my job?": """
    Climate change can lead to economic shifts that affect job markets. Certain industries might shrink or grow, and remote work opportunities may increase. The app provides an overview of how your job might be affected based on these potential changes.
    """,
    "What does the relocation recommendation score mean?": """
    The relocation recommendation score (1-100) indicates how advisable it is for you to consider moving to a different location based on climate change predictions. A higher score suggests that relocation might be a beneficial option.
    """
}

st.header("Frequently Asked Questions (FAQs)")
selected_faq = st.selectbox("", list(faq_options.keys()))

st.write(faq_options[selected_faq])

# End streamlit tracking
streamlit_analytics.stop_tracking(unsafe_password=os.getenv("STREAMLIT_TRACKING_PASSWORD"),
                                  firestore_collection_name="analytics", firestore_key_file=os.getenv("FIRESTORE_JSON"),
                                  save_to_json="setup/analytics_results.json")
