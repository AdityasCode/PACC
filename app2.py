import os

# Load environment variables
from dotenv import load_dotenv
from flask import Flask, request, render_template
from openai import OpenAI

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

# Initialize Flask app
app = Flask(__name__)

# Function to get GPT output
system_msg = {
    "role": "system",
    "content": (
        "You are a bot that estimates climate change effects on various aspects of a person's life, integrated into a "
        "climate change prediction app. Your purpose is to provide concise, to-the-point responses regarding the "
        "ecological impact of climate change. A user will talk to my app, and give their city/state/country, age, "
        "medical conditions, net worth, asset worth, job, and likelihood of getting another job. I will then tell you"
        "how many years into the future you should predict. Only answer with your predictions, no greetings, no other "
        "phrases and nothing else. if you happen to receive missing or invalid input or something that does not sound real or "
        "fitting, simply reply with 'invalid/insufficient/missing input'. Give answers as detailed as possible, but do "
        "not give false information. try to keep it above 30-40 words, but if not possible, then leave as such. "
        "if someone is retired or unemployed or a student or a similar understandable and "
        "realistic predicament for not having a job, then suggest something general. if someone has no medical "
        "conditions, suggest something general. and if someone does not provide an appropriate amount of years into the"
        " future, i.e. >25 or <1, assume they mean 1 year. if they do not provide a location you can identify, use the "
        "general global trend and use most popular cities in the world for the relocation. if someone fails to provide "
        "an age between 13 and 120, default to 25 and mention 'Defaulting to 25 years old.' Similarly, default to 0 "
        "for net and asset worths and mention it, and default to no medical conditions if you cannot understand or they"
        " have not given sufficient information on that."
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


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    inputs = {
        "location": request.form.get('location'),
        "age": request.form.get('age'),
        "medical_conditions": request.form.get('medical_conditions'),
        "net_worth": request.form.get('net_worth'),
        "asset_worth": request.form.get('asset_worth'),
        "job": request.form.get('job'),
        "job_likelihood": request.form.get('job_likelihood'),
        "years_into_future": request.form.get('years_into_future')
    }

    # Input checking
    for key, value in inputs.items():
        if not value:
            inputs[key] = "Not provided"

    predictions = {}
    for key, value in inputs.items():
        predictions[key] = value

    location = predictions["location"]
    years_future = predictions["years_into_future"]
    medical_conditions = predictions["medical_conditions"]
    job = predictions["job"]
    net_worth = predictions["net_worth"]
    asset_worth = predictions["asset_worth"]
    ecological_prompt = str(
        f"Describe the ecological impact on {location} in {years_future} years due to climate change.")
    ecological_impact = get_gpt_output(ecological_prompt)

    medical_prompt = str(
        f"Describe how {medical_conditions} in {location} might be impacted by climate change in {years_future} years.")
    medical_impact = get_gpt_output(medical_prompt)

    job_prompt = str(
        f"Describe how a {job} might be impacted by climate change in {years_future} years.")
    job_impact = get_gpt_output(job_prompt)

    relocation_prompt = str(
        f"Recommend whether a person with ${net_worth} in bank account and ${asset_worth} in assets should relocate"
        f" due to climate change in {years_future} years, and suggest nearby locations. also try to create a relocation"
        f" score out of 100 on which you think they should relocate basis all this info.")
    relocation_recommendation = get_gpt_output(relocation_prompt)

    modification_prompt = str(
        f"Suggest modifications for living space, daily lifestyle, or diet to prepare for climate change effects in"
        f" {years_future} years.")
    modifications = get_gpt_output(modification_prompt)

    responses = {
        f"Ecological Impact on {location} in {years_future} years": ecological_impact,
        f"Impact on Medical Conditions in {years_future} years": medical_impact,
        f"Impact on Job in {years_future} years": job_impact,
        "Relocation Recommendation": relocation_recommendation,
        "Modifying Your Living Space, Daily Lifestyle, or Diet": modifications
    }

    return render_template('index.html', responses=responses)


if __name__ == '__main__':
    app.run(debug=True)
