import tkinter as tk
from tkinter import scrolledtext, ttk
import threading
import json
from image_utils import ImageUtils
# from speech_utils import SpeechUtils

class ChatGUI:
    def __init__(self, root, conversation_handler):
        self.root = root
        self.conversation_handler = conversation_handler
        self.conversation_history = []
        self.setup_gui()
        
    def setup_gui(self):
        self.root.title("Chat Assistant")
        self.root.geometry("300x200")
        
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=5)
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        self.chat_display = scrolledtext.ScrolledText(
            self.main_frame,
            wrap=tk.WORD,
            height=30,
            font=("Arial", 10)
        )
        self.chat_display.grid(row=0, column=0, columnspan=2, sticky="nsew", pady=5)
        self.chat_display.config(state=tk.DISABLED)
        
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=5)
        
        
        self.input_frame = ttk.Frame(self.main_frame)
        self.input_frame.grid(row=2, column=0, columnspan=2, sticky="ew")
        
        self.message_input = ttk.Entry(
            self.input_frame,
            font=("Arial", 10)
        )
        self.message_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        self.send_btn = ttk.Button(
            self.input_frame,
            text="Send",
            command=self.send_message
        )
        self.send_btn.pack(side=tk.RIGHT)
        
        self.message_input.bind("<Return>", lambda e: self.send_message())
        
        self.append_to_chat("Assistant: Welcome to the Elon AGI. You can automate tasks such as mouse movement, clicks, and analyze your current screen.\n")

    def append_to_chat(self, message):
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, message + "\n")
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)
    
    def take_screenshot_gui(self):
        result = json.loads(ImageUtils.take_screenshot())
        self.append_to_chat(f"Screenshot saved as {result['filename']}")
    
    def show_error(self, error_message):
        self.append_to_chat(f"Error: {error_message}")
    
    def process_message(self, user_input):
        try:
            messages, should_end = self.conversation_handler.process_user_input(
                user_input,
                self.conversation_history
            )
            self.conversation_history = messages
            
            latest_response = messages[-1]
            if latest_response['role'] == 'assistant' and latest_response.get('content'):
                self.root.after(0, lambda: self.append_to_chat(f"Assistant: {latest_response['content']}"))
            
            if should_end:
                self.root.after(0, self.root.quit)
                
        except Exception as error:
            self.root.after(0, lambda: self.show_error(str(error)))
    
    def send_message(self):
        message = self.message_input.get().strip()
        if message:
            self.message_input.delete(0, tk.END)
            self.append_to_chat(f"You: {message}")
            threading.Thread(target=self.process_message, args=(message,), daemon=True).start()
    
    # def listen_for_speech(self):
    #     """Handle microphone input"""
    #     def listen():
    #         self.mic_btn.configure(state='disabled', text="🔴")
    #         result = json.loads(SpeechUtils.listen_for_input())
            
    #         if "error" in result:
    #             self.root.after(0, lambda: self.show_error(result["error"]))
    #         else:
    #             self.root.after(0, lambda: self.message_input.insert(0, result["text"]))
            
    #         self.root.after(0, lambda: self.mic_btn.configure(state='normal', text="🎤"))
        
    #     threading.Thread(target=listen, daemon=True).start()
