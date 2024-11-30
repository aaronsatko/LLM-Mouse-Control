import openai
import json
from config import Config
import os
import logging
from image_utils import ImageUtils

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OpenAIHandler:
    def __init__(self):
        if not Config.API_KEY:
            raise ValueError("API key is required to use OpenAI's API")
        openai.api_key = Config.API_KEY

    def analyze_screenshot(self, arguments):     
        image_path = None
        prompt = arguments.get("prompt", "What is in this image?")
        detail = arguments.get("detail", "auto")
        take_screenshot = True

        if take_screenshot:
            screenshot_data = json.loads(ImageUtils.take_screenshot())
            image_path = screenshot_data["filename"]
        
        try:
            base64_image = ImageUtils.encode_image(image_path)
            response = openai.chat.completions.create(
                model=Config.MODEL,
                messages=[{
                    "role": "user",
                    "content": [{
                        "type": "text",
                        "text": prompt,
                    }, {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}",
                            "detail": detail
                        },
                    }],
                }],
                max_tokens=500
            )
            
            ImageUtils.delete_screenshot()
            return response.choices[0].message.content
        except Exception as e:
            if take_screenshot and image_path and os.path.exists(image_path):
                ImageUtils.delete_screenshot()
            raise e

    def get_completion(self, messages, temperature=0, max_tokens=300, tools=None, tool_choice=None):
        response = openai.chat.completions.create(
            model=Config.MODEL,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            tools=tools,
            tool_choice=tool_choice
        )
        return response.choices[0].message
