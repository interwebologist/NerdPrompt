# NerdPrompt

**AI formatted for riced out terminals now with customizable ANSI colors, emoji's, ASCII art, Code detection and code syntax highlighting**

Welcome to **NerdPrompt**, a project that brings the power of AI into your elevated terminal. This tool allows you to query your AI and receive beautifully formatted responses with colorful ANSI colors, Emoji and/or ASCII art dividers and bullet points, Code detection and syntax highlighting with its own divider. Think markdown headers, bold, italics, dividers, and code blocks , but turned WAY up and customizable.


NerdPrompt: AI in terminal featuring:
Rich Emoji, ANSI and ASCII Art color formatting replacement for Markdown formatting of headers, bold, italics, bullets,and dividers

![Alt text](images/7.png "Optional title")
![Alt text](images/5.png "Optional title")
![Alt text](images/4.png "Optional title")
![Alt text](images/1.png "Optional title")
![Alt text](images/2.png "Optional title")
![Alt text](images/6.png "Optional title")

---

## 🚀 Features

- **Custom Emoji,ANSI (Colors), or ASCII-enhanced bullet points** 
- **Customer Multi-colored headers** using ANSI formatting you can match your VIM or terminal theme for headers 1, 2 and 3:
- Supports **bold**, *italic*, and ***bold italic*** text rendered directly in the terminal.
- Removes citation markers like `[^1]` for a cleaner output in perplexity.ai (clickable links coming in future release)
- Code syntax highlighting with language detection. Custom dividers set in config for blocks of code.
- Easy-to-use interface for querying Perplexity.ai.

---

## 🔧 Installation

Follow these steps to install Nerd Prompt:

1. **Clone the repository:**

    ```
    git clone https://github.com/your-repo/perplexed-terminal.git
    cd perplexed-terminal
    ```

2. **Create and activate a virtual environment (recommended):**

    ```
    python3 -m venv venv
    # On Linux or macOS:
    source venv/bin/activate
    # On Windows:
    venv\Scripts\activate
    ```

3. **Install dependencies:**

    ```
    pip install -r requirements.txt
    ```

4. **Set up your API key (see below).**

---

**Note:**  
Using a virtual environment (`venv`) keeps dependencies isolated from your system Python and is best practice for Python projects.

---

## 🔑 Setting Up Your API Key

To use **Nerd Prompt**, you need an API key from Perplexity.ai. Here's how to get it:

1. **Log in to Perplexity.ai**: Visit [www.perplexity.ai](https://www.perplexity.ai) and log in to your account.
2. **Navigate to Settings**: Click on the **Settings** icon (bottom-left corner).
3. **Access the API Tab**: Select the **API** tab from the menu.
4. **Generate or Copy Your API Key**: Click "Generate API Key" if you don't already have one, or copy your existing key.
5. Save your API key securely.

---

## 🛠️ Configuring Your API Key

1. Create a `.env` file in the project directory:

```bash
touch .env
```

2. Add your API key to the `.env` file:

```plaintext
API_KEY=your_api_key_here
```

3. The project will automatically load the key from the `.env` file when you run it.

---

## 🖥️ Usage Instructions

Run the script with your query as an argument:

```bash
python nerd_prompt.py "What is the capital of France?"
```
---

## ✨ Markdown Formatting in Terminal

The tool supports formatting for the Terminal:

- **Headers** are styled with different colors. Example:
    - Green for `# Header`
    - Blue for `## Subheader`
    - Red for `### Sub-subheader`
- Text styling includes:
    - **Bold**
    - *Italic*
    - ***Bold Italic***
- Emoji-enhanced bullet points like 🚀, 🔥, and ✨ add personality to your terminal output.
- Add your own ASCII art dividers or dividers with emoji's

---

## 💡 Best Practices

- Keep your API key private—do not share it publicly.
- Ensure you have sufficient credits in your Perplexity.ai account to make queries.
- Use Python 3.8 or higher for compatibility.

---

## ❓ Troubleshooting

If you encounter issues:

1. Ensure your `.env` file contains a valid API key.
2. Verify that all dependencies are installed (`pip install -r requirements.txt`).
3. Check your Perplexity.ai account for sufficient credits or active API keys.

For further assistance, consult [Perplexity's Help Center](https://www.perplexity.ai/help-center).

---

## 🎨 Code Syntax Highlighting Themes

This project uses [Pygments](https://pygments.org/) for code syntax highlighting. You can customize the appearance of code blocks by selecting one of the many available Pygments styles. For a live preview of each theme, visit the [Pygments demo page](https://pygments.org/demo/)[4][15].

**To set a style, configure your formatter in the config.yaml with the desired style name.**  
For example, in Python:

[9][5]

### Available Code Styles

Below is a list of supported syntax highlighting themes:

- abap
- algol
- algol_nu
- arduino
- autumn
- bw
- borland
- coffee
- colorful
- default
- dracula
- emacs
- friendly_grayscale
- friendly
- fruity
- github-dark
- gruvbox-dark
- gruvbox-light
- igor
- inkpot
- lightbulb
- lilypond
- lovelace
- manni
- material
- monokai
- murphy
- native
- nord-darker
- nord
- one-dark
- paraiso-dark
- paraiso-light
- pastie
- perldoc
- rainbow_dash
- rrt
- sas
- solarized-dark
- solarized-light
- staroffice
- stata-dark
- stata-light
- tango
- trac
- vim
- vs
- xcode
- zenburn

Enjoy using **Nerd Prompt**! 🚀
