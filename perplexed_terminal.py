from dotenv import load_dotenv
from openai import OpenAI
import os
import string 
import sys
import re
 
class PerplexityWrapper:
    def __init__(self, api_key):
        self.api_key = api_key
 
    def client(self, your_question):
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
        
        client = OpenAI(api_key=self.api_key, base_url="https://api.perplexity.ai")
    
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
        markdown_text = re.sub(r'^\s*[-*+]\s*', f" {UNICODE_CODES['bullet']} ", markdown_text, flags=re.MULTILINE)
    
        return markdown_text
    def remove_citations(self, dirty_response):
        
        # Remove citation markers (e.g., [1], [2]) from text
        clean_response = re.sub(r'\[\d+\]', '', dirty_response)
        return clean_response

    # Scrub code from the text to avoid turn comments in headers.
    def code_extractor(self, text):
        code_blocks = []
        code_block_count = 0
        
        pattern = r'```[\s\S]*?```'
        while True:
            match = re.search(pattern, text)
            if match:
                code_blocks.append(match.group(0))
                escaped_string = re.escape(match.group(0))
                text = re.sub(escaped_string, f'<CODE__REMOVED__{code_block_count}>', text, count=1, flags=re.DOTALL)
                code_block_count = code_block_count+1
            else:
                return {"text": text,"code_blocks": code_blocks }
    
    # Takes dict with doc and code blocks and puts them back together.
    # Stylize header before this functions or Python comments become headers
    def code_injector(self, doc_and_code_blocks):
        input_text = doc_and_code_blocks['new_text']
        code_block_count = 0
        for code_block in doc_and_code_blocks['code_blocks']:
                input_text = input_text.replace(f'<CODE__REMOVED__{code_block_count}>',code_block)
                code_block_count = code_block_count+1
        return input_text 
def main():
    #sys.argv[1] = "show me the smallest OOP python script you can "
    try:
        # Load environment variables from .env file
        load_dotenv()
        YOUR_API_KEY = os.environ["API_KEY"]
    except KeyError:
        print("Error: API_KEY is missing from the environment variables.")
        sys.exit(1)

    if len(sys.argv) < 1:
        print('Usage: python ask_perplexity.py "your question here"')
        sys.exit(1)
    try:
        #your_question = sys.argv[1]
        your_question = "show me the smallest oop python script you can "#sys.argv[1]
    except ValueError:
        print('Use qoutes: python ask_perplexity.py "your question here"')
    try:
        perplexity_client = PerplexityWrapper(YOUR_API_KEY)
        response = perplexity_client.client(your_question)
        content = response.choices[0].message.content
        doc_wo_code = perplexity_client.code_extractor(content)
        doc_no_code = doc_wo_code['text']
        ansi_text = perplexity_client.markdown_to_ansi(doc_no_code)
        ansi_doc_no_code = doc_wo_code
        ansi_doc_no_code['new_text'] = ansi_text
        doc_with_code = perplexity_client.code_injector(ansi_doc_no_code)
        no_citation_ansi_text = perplexity_client.remove_citations(doc_with_code)
        print(no_citation_ansi_text)
    except Exception as e:
        print(f"An error occurred: {e}")
    
if __name__ == "__main__":
    
    main()
