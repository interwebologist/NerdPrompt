import traceback
from pygments import highlight
from pygments.lexers import guess_lexer, get_lexer_by_name
from pygments.formatters import Terminal256Formatter
from cerberus import Validator
from dotenv import load_dotenv
import pygments
from openai import OpenAI
import yaml
import os
import string 
import sys
import re
 
class PerplexityWrapper:
    def __init__(self, api_key):
        self.api_key = api_key
 
    def client(self, config,  your_question):
        messages = [
            {
                "role": "system",
                "content": (
                 f"""{config['system_content']}"""
                ),
            },
            {   
                "role": "user",
                "content": (
                    your_question
                ),
            },
        ]
        
        client = OpenAI(api_key=self.api_key, base_url=f"{config['llm_url']}")
    
        # chat completion without streaming
        response = client.chat.completions.create(
            model=f"{config['llm_model']}",
            messages=messages,
        #    stream=True, #Streaming disabled
        )
        return response
    
    def markdown_to_ansi(self, ansi_codes, config, markdown_text):
        # Define ANSI escape codes for colors and styles

        # Convert headers to bold and colored
        markdown_text = re.sub(r'(?m)^# (.+)$', 
                               f"{ansi_codes['bold']}{ansi_codes['green']}\\1{ansi_codes['reset']}", 
                               markdown_text)
        markdown_text = re.sub(r'(?m)^## (.+)$', 
                               f"{ansi_codes['bold']}{ansi_codes['blue']}\\1{ansi_codes['reset']}", 
                               markdown_text)
        markdown_text = re.sub(r'(?m)^### (.+)$', 
                               f"{ansi_codes['bold']}{ansi_codes['red']}\\1{ansi_codes['reset']}", 
                               markdown_text)
    
        # Convert bold and italic text (***) first to avoid conflicts
        markdown_text = re.sub(r'\*\*\*(.+?)\*\*\*', 
                               f"{ansi_codes['bold_italic']}\\1{ansi_codes['reset']}", 
                               markdown_text)
    
        # Convert bold text (**text**)
        markdown_text = re.sub(r'\*\*(.+?)\*\*', 
                               f"{ansi_codes['bold']}\\1{ansi_codes['reset']}", 
                               markdown_text)
    
        # Convert italic text (*text*)
        markdown_text = re.sub(r'\*(.+?)\*', 
                               f"{ansi_codes['italic']}\\1{ansi_codes['reset']}", 
                               markdown_text)
        
        # Divider choice 
        ascii_divider_choice = config['ascii_divider_choice']  
        ascii_divider = config["ascii_dividers"][ascii_divider_choice]
        # Divider --- 
        markdown_text = re.sub(r'^---$', rf"{ascii_divider}", markdown_text, flags = re.MULTILINE) 
        # Bullet -  
        markdown_text = re.sub(r'^\s*-\s+', f" {config['bullet_point_unicode']} ", markdown_text, flags=re.MULTILINE)
        
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
        md_without_code = doc_and_code_blocks['ansi_converted_text']
        code_block_count = 0
        for code_block in doc_and_code_blocks['code_blocks']:
                md_without_code = md_without_code.replace(f'<CODE__REMOVED__{code_block_count}>',code_block)
                code_block_count = code_block_count+1
        md_with_code = md_without_code
        return md_with_code

class CodeProcesser:    
    # remove code type (```python.....````) from markup and split out code for syntax highligting 
    def extract_code_type_and_syntax(self, input_string):
        pattern = r'```([A-Za-z]*)([\s\S.]*)```'  # Adjusted to handle closing ```
        match = re.search(pattern, input_string, re.DOTALL)
        if match:
            return {
                'code_type': match.group(1),
                'code_syntax': match.group(2)
            }
        return None
    
    # Syntax highlighting the 'guts' for the code markdown.first try explict then guess
    def syntax_highlighter(self, config, code_type_and_syntax):
        try:
            lexer = get_lexer_by_name(code_type_and_syntax['code_type'])
        except:
            lexer = guess_lexer(code_type_and_syntax['code_syntax'])   
        finally:
            #formatter = TerminalFormatter(style = f"{config['code_syntax_theme']}")
            formatter = Terminal256Formatter(style = f"{config['code_syntax_theme']}")
        highlighted_code = highlight(code_type_and_syntax['code_syntax'], lexer, formatter)
        code_type_and_syntax['highlighted_code'] = highlighted_code
        return code_type_and_syntax

    # We need to piece the highlighted markdown back together ```python\n<code></code>``` and put it 
    # back in doc converted to ANSI so  code displays highlighted
    # Added config.yaml code_dividers. This surrounds code blocks and doesn't replace --- markdown
    def rebuild_code_type_and_syntax(self, ansi_codes, config, extracted_code):
        code_type = extracted_code['code_type'].capitalize()
        code_syntax = extracted_code['highlighted_code']
        code_divider_choice = config["code_divider_choice"]
        code_divider = config["code_dividers"][code_divider_choice]
        rebuilt_code=f"""{code_divider}\n{code_type} Code:\n{code_syntax}\n{code_divider}\n"""
        return rebuilt_code

class ConfigEater:
    def parse_config(self):
          with open('config.yaml', 'r') as f:
              config = yaml.safe_load(f)
              return config
    def check_config(self, config_dict):
        schema = {
        'llm_url': {'type': 'string', 'required': True},
        'llm_model': {'type': 'string', 'required': True},
        'remove_perplexity_citations': {'type': 'boolean', 'required': True},
        'code_syntax_theme': {'type': 'string', 'required': True},
        'system_content': {'type': 'string', 'required': True},
        'bullet_point_unicode': {'type': 'string', 'required': True},
        'header_1': {'type': 'list', 'schema': {'type': 'string'}, 'required': True},
        'header_2': {'type': 'list', 'schema': {'type': 'string'}, 'required': True},
        'header_3': {'type': 'list', 'schema': {'type': 'string'}, 'required': True},
        'ascii_divider_position': {'type': 'string', 'allowed': ['left', 'center', 'right'], 'required': True},
        'ascii_divider_choice': {'type': 'integer', 'required': True},
        'ascii_dividers': {
            'type': 'dict',
            'keysrules': {'type': 'integer'},
            'valuesrules': {'type': 'string'},
            'required': True
        },
        'code_divider_choice': {'type': 'integer', 'required': True},
        'code_dividers': {
            'type': 'dict',
            'keysrules': {'type': 'integer'},
            'valuesrules': {'type': 'string'},
            'required': True
        },
        }
    
        v = Validator(schema)
        is_valid = v.validate(config_dict)
    
        if not is_valid:
            raise ValueError(f"Config validation error: {v.errors}") 

def main():
    config_eater = ConfigEater()
    config = config_eater.parse_config()
    config_eater.check_config(config)
   
    ansi_codes = {
    'bold': '\033[1m',
    'italic': '\033[3m',
    'bold_italic': '\033[1;3m',
    'underline': '\033[4m',
    'green': '\033[32m',
    'blue': '\033[34m',
    'red': '\033[31m',
    'yellow': '\033[33m',
    'magenta': '\033[35m',
    'cyan': '\033[36m',
    'white': '\033[37m',
    'black': '\033[30m',
    'bg_red': '\033[41m',
    'bg_green': '\033[42m',
    'bg_yellow': '\033[43m',
    'bg_blue': '\033[44m',
    'bg_magenta': '\033[45m',
    'bg_cyan': '\033[46m',
    'bg_white': '\033[47m',
    'bg_black': '\033[40m',
    'strikethrough': '\033[9m',
    'reverse': '\033[7m',
    'conceal': '\033[8m',
    'reset': '\033[0m',
    }
 
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
        your_question = sys.argv[1]
        #your_question = "show me denver weather using bullet points and dividers included" #sys.argv[1]
    except ValueError:
        print('Use qoutes: python ask_perplexity.py "your question here"')
    try:
        perplexity_client = PerplexityWrapper(YOUR_API_KEY)
        
        response = perplexity_client.client(config, your_question)
        content = response.choices[0].message.content
        doc_wo_code = perplexity_client.code_extractor(content)
        
        doc_no_code_str = doc_wo_code['text'] #doc without code
        ansi_text = perplexity_client.markdown_to_ansi( ansi_codes, config, doc_no_code_str) #doc with no code converted to ANSI
        doc_wo_code['ansi_converted_text'] = ansi_text #adding dict key for ANSI converted text
       
        # todo: check code processing can happen when streaming since we cannot detect opening a closing markdown
        # in events
        code_processing = CodeProcesser()
        rebuilt_code_blocks = []
        for code in doc_wo_code['code_blocks']: #process code, 1. take apart markdown 2. explict code highlight 2. reconstruct 3 add to ANSI text
            code_type_and_syntax = code_processing.extract_code_type_and_syntax(code)
            highlighted_syntax = code_processing.syntax_highlighter(config, code_type_and_syntax)
            rebuilt_code = code_processing.rebuild_code_type_and_syntax( ansi_codes, config, highlighted_syntax)
            rebuilt_code_blocks.append(rebuilt_code)
            # Replace the original code_blocks with the rebuilt ones
        doc_wo_code['code_blocks'] = rebuilt_code_blocks

        doc_with_code = perplexity_client.code_injector(doc_wo_code)
        no_citation_ansi_text = perplexity_client.remove_citations(doc_with_code)
        print(no_citation_ansi_text)
    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc() 
    
if __name__ == "__main__":
    
    main()

