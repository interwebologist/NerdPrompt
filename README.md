# Nerd Prompt

![Perplexity Logo](https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png)

**Perplexity.ai formatted in terminal with emoji and ANSI formatting**

Welcome to **Nerd Prompt**, a Python-based project that brings the power of Perplexity.ai into your terminal. This tool allows you to query Perplexity.ai and receive beautifully formatted responses with emojis, ANSI colors, and Markdown styling directly in your terminal.

---

## 🚀 Features

- **Emoji-enhanced bullet points** for a fun and engaging experience.
- **Multi-colored headers** using ANSI formatting:
    - Green for `# Header`
    - Blue for `## Subheader`
    - Red for `### Sub-subheader`
- Supports **bold**, *italic*, and ***bold italic*** text rendered directly in the terminal.
- Removes citation markers like `[^1]` for a cleaner output.
- Easy-to-use interface for querying Perplexity.ai.

---

## 🔧 Installation

Follow these steps to install **Nerd Prompt**:

1. Clone the repository:

```bash
git clone https://github.com/your-repo/perplexed-terminal.git
cd perplexed-terminal
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set up your API key (see below).

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
python perplexed_terminal.py "What is the capital of France?"
```


### Example Output:

```plaintext
# 🌟 Paris
Paris is the capital city of France.

## 🗺️ Geography
Located along the Seine River, Paris is known for its iconic landmarks like the Eiffel Tower.

### 🎨 Culture
Paris is also a global center for art, fashion, and gastronomy.
```

---

## ✨ Markdown Formatting in Terminal

The tool supports rich Markdown formatting with ANSI colors:

- **Headers** are styled with different colors:
    - Green for `# Header`
    - Blue for `## Subheader`
    - Red for `### Sub-subheader`
- Text styling includes:
    - **Bold**
    - *Italic*
    - ***Bold Italic***
- Emoji-enhanced bullet points like 🚀, 🔥, and ✨ add personality to your terminal output.

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

Enjoy using **Nerd Prompt**! 🚀

<div>⁂</div>
# Pygment Python Library syntax styles setting. Mark code block will be colored with this theme
# Check what these would look like by using the Pygment style checker. Check which syntax type
# "Python" , etc and use the dropdown to check themes. https://pygments.org/demo/. If extra styles
# are added just add them below in a new numbered line and set code_syntax_choice to style number.
Code Syntax Highlighting Themes
```
  1: "abap"
  2: "algol"
  3: "algol_nu"
  4: "arduino"
  5: "autumn"
  6: "bw"
  7: "borland"
  8: "coffee"
  9: "colorful"
  10: "default"
  11: "dracula"
  12: "emacs"
  13: "friendly_grayscale"
  14: "friendly"
  15: "fruity"
  16: "github-dark"
  17: "gruvbox-dark"
  18: "gruvbox-light"
  19: "igor"
  20: "inkpot"
  21: "lightbulb"
  22: "lilypond"
  23: "lovelace"
  24: "manni"
  25: "material"
  26: "monokai"
  27: "murphy"
  28: "native"
  29: "nord-darker"
  30: "nord"
  31: "one-dark"
  32: "paraiso-dark"
  33: "paraiso-light"
  34: "pastie"
  35: "perldoc"
  36: "rainbow_dash"
  37: "rrt"
  38: "sas"
  39: "solarized-dark"
  40: "solarized-light"
  41: "staroffice"
  42: "stata-dark"
  43: "stata-light"
  44: "tango"
  45: "trac"
  46: "vim"
  47: "vs"
  48: "xcode"
  49: "zenburn"
```
