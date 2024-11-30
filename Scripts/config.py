import os
from pathlib import Path

class Config:
    # Base Directories
    BASE_DIR = Path(__file__).parent.absolute()
    SCREENSHOT_DIR = os.path.join(BASE_DIR, "screenshot")
    ARCHIVE_DIR = os.path.join(BASE_DIR, "archive")
    
    # API Configuration
    API_KEY = os.getenv("OPENAI_API_KEY")
    MODEL = "gpt-4o-mini"

    # GUI Configuration
    GUI_CONFIG = {
        "window_title": "Multi-Function Assistant",
        "window_size": "800x600",
        "font_family": "Arial",
        "font_size": 10,
        "chat_height": 30,
        "padding": {"x": 10, "y": 5}
    }

    # Functions Configuration
    FUNCTIONS = [
        {
            "name": "take_screenshot",
            "description": "Takes a screenshot and saves it with a timestamped filename.",
            "parameters": {"type": "object", "properties": {}, "required": []}
        },
        {
            "name": "analyze_screenshot",
            "description": "Analyzes a screenshot's content.",
            "parameters": {
                "type": "object",
                "properties": {
                    "prompt": {"type": "string", "description": "Prompt for analysis"},
                    "detail": {
                        "type": "string",
                        "enum": ["low", "high", "auto"],
                        "description": "Level of detail for analysis"
                    }
                },
                "required": []
            }
        },
        {
            "name": "delete_screenshot",
            "description": "Deletes screenshot files.",
            "parameters": {"type": "object", "properties": {}, "required": []}
        },
        {
            "name": "end_conversation",
            "description": "Ends the conversation with the user.",
            "parameters": {"type": "object", "properties": {}, "required": []}
        },
        {
            "name": "move_mouse_to",
            "description": "Move mouse to absolute screen coordinates.",
            "parameters": {
                "type": "object",
                "properties": {
                    "x": {"type": "integer", "description": "X coordinate on screen"},
                    "y": {"type": "integer", "description": "Y coordinate on screen"},
                    "duration": {
                        "type": "number",
                        "description": "Time to take for movement in seconds",
                        "default": 0.5
                    }
                },
                "required": ["x", "y"]
            }
        },
        {
            "name": "move_mouse_relative",
            "description": "Move mouse relative to current position.",
            "parameters": {
                "type": "object",
                "properties": {
                    "x_offset": {
                        "type": "integer",
                        "description": "Horizontal offset from current position"
                    },
                    "y_offset": {
                        "type": "integer",
                        "description": "Vertical offset from current position"
                    },
                    "duration": {
                        "type": "number",
                        "description": "Time to take for movement in seconds",
                        "default": 0.5
                    }
                },
                "required": ["x_offset", "y_offset"]
            }
        },
        {
            "name": "get_mouse_position",
            "description": "Get current mouse cursor coordinates.",
            "parameters": {"type": "object", "properties": {}, "required": []}
        },
        {
            "name": "click",
            "description": "Click at current position or specified coordinates.",
            "parameters": {
                "type": "object",
                "properties": {
                    "x": {"type": "integer", "description": "X coordinate to click at"},
                    "y": {"type": "integer", "description": "Y coordinate to click at"}
                },
                "required": []
            }
        },
        {
            "name": "double_click",
            "description": "Double click at current position or specified coordinates.",
            "parameters": {
                "type": "object",
                "properties": {
                    "x": {"type": "integer", "description": "X coordinate to double click at"},
                    "y": {"type": "integer", "description": "Y coordinate to double click at"}
                },
                "required": []
            }
        },
        {
            "name": "get_system_info",
            "description": "Get system information including screen dimensions.",
            "parameters": {"type": "object", "properties": {}, "required": []}
        },
        {
            "name": "find_and_center_target",
            "description": "Takes screenshots and moves mouse to center on a target through multiple iterations.",
            "parameters": {
                "type": "object",
                "properties": {
                    "target": {"type": "string", "description": "Description of what to look for"},
                    "max_attempts": {
                        "type": "integer",
                        "description": "Maximum number of attempts to center",
                        "default": 5
                    }
                },
                "required": ["target"]
            }
        }
    ]

    # Build TOOLS list from FUNCTIONS
    TOOLS = [{"type": "function", "function": func} for func in FUNCTIONS]

    # OpenAI API Configuration
    OPENAI_CONFIG = {
        "temperature": 0,
        "max_tokens": 300,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0
    }

    @classmethod
    def initialize(cls):
        os.makedirs(cls.SCREENSHOT_DIR, exist_ok=True)
        os.makedirs(cls.ARCHIVE_DIR, exist_ok=True)
        if not cls.API_KEY:
            raise ValueError("OpenAI API key not found. Set the OPENAI_API_KEY environment variable.")
