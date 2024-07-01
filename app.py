import streamlit as st
import time

# Set page configuration
st.set_page_config(
    page_title="Climate Change Impact Predictions",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Title and description
st.title("🌍 Climate Change Impact Predictions 🌿")
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
medical_conditions = st.text_area("List your medical conditions:", placeholder="Enter your medical conditions, separated by commas")

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
        with st.spinner('Calculating predictions... Please wait...'):
            time.sleep(12)  # Simulating computation time

        # Hard-coded output
        st.header("Predictions")

        st.subheader(f"Ecological Impact on San Francisco in {years_future} years")
        st.write(f"""
        In {years_future} years, San Francisco is expected to experience significant ecological changes due to climate change. Rising sea levels and increased frequency of extreme weather events will likely affect coastal areas, leading to flooding and infrastructure damage.
        """)

        st.subheader(f"Impact on Medical Conditions in {years_future} years")
        st.write(f"""
        With asthma and an early stage of MS, you might experience worsened symptoms due to increased air pollution and higher temperatures over the next {years_future} years. It's essential to stay in a well-ventilated and climate-controlled environment.
        """)

        st.subheader(f"Impact on Job in {years_future} years")
        st.write(f"""
        As a senior software engineer at NeXT and Sun Microsystems, your job might be affected by changes in the tech industry driven by climate change over the next {years_future} years. Remote work opportunities may increase, but job security could be influenced by economic instability.
        """)

        st.subheader("Relocation Recommendation")
        relocation_recommendation = 70
        nearby_locations = ["Portland, OR", "Seattle, WA", "Denver, CO"]
        st.write(f"""
        Based on your input, we recommend a relocation score of {relocation_recommendation}/100. Consider moving to one of these nearby locations: {", ".join(nearby_locations)}.
        """)

        st.subheader("Modifying Your Living Space, Daily Lifestyle, or Diet")
        st.write(f"""
        To prepare for the effects of climate change over the next {years_future} years, consider implementing the following changes:
        - Improve insulation and ventilation in your home.
        - Reduce energy consumption and use renewable energy sources.
        - Adopt a diet rich in fruits, vegetables, and sustainable food sources.
        - Stay informed about air quality and avoid outdoor activities during high pollution periods.
        """)

