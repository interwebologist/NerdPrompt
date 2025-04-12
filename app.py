from dotenv import load_dotenv
from openai import OpenAI
import os
import string 

# Load environment variables from .env file
load_dotenv()
#
YOUR_API_KEY = os.environ["API_KEY"]

your_question = input("What would you like to ask? ")

messages = [
    {
        "role": "system",
        "content": (
         """You are an artificial intelligence assistant and you need to
            engage in a helpful, detailed, polite conversation with a user."""
        ),
    },
    {   
        "role": "user",
        "content": (
            your_question
        ),
    },
]

client = OpenAI(api_key=YOUR_API_KEY, base_url="https://api.perplexity.ai")

# chat completion without streaming
response = client.chat.completions.create(
    model="sonar-pro",
    messages=messages,
#    stream=True, #Streaming disabled
)

print(response.choices[0].message.content)
