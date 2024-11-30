import json
from datetime import datetime
from image_utils import ImageUtils
from openai_handler import OpenAIHandler
from mouse_utils import MouseUtils
from config import Config

class ConversationHandler:
    def __init__(self, openai_handler):
        self.openai_handler = openai_handler
        self.system_info = self.get_system_info()

    def get_current_time(self, arguments=None):
        current_time = datetime.now().strftime("%H:%M:%S")
        return json.dumps({"current_time": current_time})

    def end_conversation(self, arguments=None):
        return json.dumps({"status": "ending", "message": "Goodbye! Have a great day!"})

    def get_system_info(self, arguments=None):
        return json.dumps({
            "screen_width": MouseUtils.SCREEN_WIDTH,
            "screen_height": MouseUtils.SCREEN_HEIGHT,
            "system_info": "Screen dimensions and other system parameters"
        })

    def execute_function(self, function_call):
        function_name = function_call.function.name
        function_args = function_call.function.arguments

        # List of modules to check
        modules = [self, ImageUtils, MouseUtils, self.openai_handler]
        func = None
        for module in modules:
            if hasattr(module, function_name):
                func = getattr(module, function_name)
                break

        if func is None:
            return json.dumps({"error": f"Unknown function {function_name}"})

        try:
            return func(function_args)
        except Exception as e:
            return json.dumps({"error": f"Error executing {function_name}: {str(e)}"})

    def process_user_input(self, user_input, conversation_history=None):
        if not conversation_history:
            conversation_history = [{
                "role": "system",
                "content": f"You have access to the following system information: {self.system_info}"
            }]
        
        messages = conversation_history + [{"role": "user", "content": user_input}]
        
        while True:
            response = self.openai_handler.get_completion(
                messages=messages,
                tools=Config.TOOLS
            )
            
            if hasattr(response, 'tool_calls') and response.tool_calls:
                for tool_call in response.tool_calls:
                    function_response = self.execute_function(tool_call)
                    
                    messages.append({
                        "role": "assistant",
                        "content": None,
                        "tool_calls": [
                            {
                                "id": tool_call.id,
                                "type": "function",
                                "function": {
                                    "name": tool_call.function.name,
                                    "arguments": tool_call.function.arguments
                                }
                            }
                        ]
                    })
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": tool_call.function.name,
                        "content": function_response
                    })
                    
                    if tool_call.function.name == "end_conversation":
                        function_result = json.loads(function_response)
                        if function_result.get("status") == "ending":
                            return messages, True
            else:
                messages.append({
                    "role": "assistant",
                    "content": response.content
                })
                break
        
        return messages, False
