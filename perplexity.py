from dotenv import load_dotenv
from openai import OpenAI
import os
import string 
import sys
import re
 
class PerplexityWrapper:
 
    def client(self, key, your_question):
        messages = [
            {
                "role": "system",
                "content": (
                 """You are an artificial intelligence assistant and you will
                    engage in a helpful, detailed, conversation with a user while 
                    using markdown for formatting"""
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
        return response
    
    def markdown_to_ansi(self, markdown_text):
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
    
        UNICODE_CODES = {
            'bullet': '\U0001F680',  # 🚀 Rocket
            'fire': '\U0001F525',  # 🔥 Fire
            'sparkles' : '\U00012728',     # ✨ Sparkles
            'green_dot' : '\U0001F7E2'  # green dot
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
        
        ### Unicode Codes
    
        # Divider --- 
        markdown_text = re.sub(r'\-\-\-', 
                               f"{UNICODE_CODES['sparkles']}-----------{UNICODE_CODES['sparkles']}", 
                               markdown_text) 
        # Divider -*+ bullets 
        markdown_text = re.sub(r'^\s*[-*+]\s*', f" {UNICODE_CODES['green_dot']} ", markdown_text, flags=re.MULTILINE)
    
        return markdown_text
    
if __name__  == "__main__":
    # Load environment variables from .env file
    load_dotenv()
    
    YOUR_API_KEY = os.environ["API_KEY"]
    
    if sys.argv[1] == None:
        print('run ask_perplexity.py "what is the weather in LA today?"')
    elif sys.argv:
        your_question = sys.argv[1]

    perplexity_client = PerplexityWrapper()

    response = perplexity_client.client(YOUR_API_KEY, your_question)  
    term_text = perplexity_client.markdown_to_ansi(response.choices[0].message.content)
    print(term_text)

