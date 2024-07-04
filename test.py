import os

import dotenv
from openai import OpenAI

dotenv.load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
print(OPENAI_API_KEY)
client = OpenAI(api_key=OPENAI_API_KEY)

# Function to get GPT output
system_msg = {
    "role": "system",
    "content": (
        "You are an AI assistant integrated into a climate change prediction app. Your purpose is to provide concise, "
        "to-the-point responses regarding the ecological impact of climate change, its effects on medical conditions, "
        "job market implications, and advice on relocation or lifestyle modifications based on user input."
    )
}

response = client.chat.completions.create(model="gpt-3.5-turbo",
                                          messages=[
                                              system_msg,
                                              {"role": "user", "content": "give SF tech job market implications of"
                                                                          "floods in SF"}
                                          ],
                                          temperature=0)
print(response.choices[0].message.content)
