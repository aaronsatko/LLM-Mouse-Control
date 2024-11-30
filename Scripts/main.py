# File: main.py
import tkinter as tk
from gui import ChatGUI
from openai_handler import OpenAIHandler
from conversation_handler import ConversationHandler
from config import Config

def main():
    if Config.API_KEY is None:
        print("Error: OPENAI_API_KEY environment variable not set.")
        return

    root = tk.Tk()
    openai_handler = OpenAIHandler()
    conversation_handler = ConversationHandler(openai_handler)
    app = ChatGUI(root, conversation_handler)
    root.mainloop()

if __name__ == "__main__":
    main()
    
