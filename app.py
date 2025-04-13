from dotenv import load_dotenv
from openai import OpenAI
import os
import string 
import sys
import re

# Load environment variables from .env file
load_dotenv()
YOUR_API_KEY = os.environ["API_KEY"]

if sys.argv[1] == None:
    print("You must ask perplexity a question. Run again")
elif sys.argv:
    your_question = sys.argv[1]

messages = [
    {
        "role": "system",
        "content": (
         """You are an artificial intelligence assistant and you need to
            engage in a helpful, detailed, polite conversation with a user.
            Use markdown for formatting"""
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

import re

def markdown_to_ansi(markdown_text):
    # Define ANSI escape codes for colors and styles
    ANSI_CODES = {
        'bold': '\033[1m',
        'italic': '\033[3m',
        'bold_italic': '\033[1;3m',
        'green': '\033[32m',
        'blue': '\033[34m',
        'red': '\033[31m',
        'reset': '\033[0m'
    }

    # Convert headers to bold and colored
    markdown_text = re.sub(r'(?m)^# (.+)$', 
                           f"{ANSI_CODES['bold']}{ANSI_CODES['green']}\\1{ANSI_CODES['reset']}", 
                           markdown_text)
    markdown_text = re.sub(r'(?m)^## (.+)$', 
                           f"{ANSI_CODES['bold']}{ANSI_CODES['blue']}\\1{ANSI_CODES['reset']}", 
                           markdown_text)
    markdown_text = re.sub(r'(?m)^### (.+)$', 
                           f"{ANSI_CODES['bold']}{ANSI_CODES['red']}\\1{ANSI_CODES['reset']}", 
                           markdown_text)

    # Convert bold and italic text (***) first to avoid conflicts
    markdown_text = re.sub(r'\*\*\*(.+?)\*\*\*', 
                           f"{ANSI_CODES['bold_italic']}\\1{ANSI_CODES['reset']}", 
                           markdown_text)

    # Convert bold text (**text**)
    markdown_text = re.sub(r'\*\*(.+?)\*\*', 
                           f"{ANSI_CODES['bold']}\\1{ANSI_CODES['reset']}", 
                           markdown_text)

    # Convert italic text (*text*)
    markdown_text = re.sub(r'\*(.+?)\*', 
                           f"{ANSI_CODES['italic']}\\1{ANSI_CODES['reset']}", 
                           markdown_text)

    return markdown_text

## Example usage
#example_markdown = """
## Header 1
### Header 2
#### Header 3
#This is **bold** text, this is *italic* text, and this is ***bold and italic*** text.
#"""

converted_text = markdown_to_ansi(response.choices[0].message.content)
print(converted_text)

