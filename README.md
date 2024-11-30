# LLM-Mouse-Control

Control your mouse effortlessly with the power of a Large Language Model (LLM). This tool enables natural language commands to control mouse actions on your screen.

---

## Features

- Execute a wide range of mouse movements and actions using simple, intuitive commands.
- Support for complex, multi-step instructions.
- Easily customizable and extendable.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/LLM-Mouse-Control.git
   cd LLM-Mouse-Control
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your OpenAI API key as an environment variable:
   ```bash
   export OPENAI_KEY=your_openai_key
   ```
   Replace `your_openai_key` with your actual OpenAI key.

---

## Usage

Run the program:
```bash
python main.py
```

Type any mouse command into the console, and the program will execute it. The tool is designed to understand a variety of natural language commands for controlling your mouse.

---

## Examples

Here are some example commands you can try:

- **Simple Movements:**
  - `Move mouse to 1000 1000`
  - `Go to the top right corner`
  - `Go half way across the screen`

- **Complex Patterns:**
  - `Move in a square`
  - `Draw a house`

- **Multi-Step Actions:**
  - `Move to 1000 1000 then double click then move to 500 500`
