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


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    prompt = request.form['prompt']
    prediction = get_gpt_output(prompt)
    return render_template('index.html', prediction=prediction)


if __name__ == '__main__':
    app.run(debug=True)
