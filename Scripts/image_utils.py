import base64
import json
import os
from datetime import datetime
from PIL import ImageGrab
from config import Config
import pyautogui
import logger

class ImageUtils:
    @staticmethod
    def encode_image(image_path):
        """Convert image to base64 string"""
        try:
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')
        except Exception as e:
            logger.error(f"Error encoding image: {str(e)}")
            raise e

    @staticmethod
    def take_screenshot(arguments=None):
        if not os.path.exists(Config.SCREENSHOT_DIR):
            os.makedirs(Config.SCREENSHOT_DIR)
        
        screenshot = ImageGrab.grab()
        filename = os.path.join(
            Config.SCREENSHOT_DIR,
            f"screenshot_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.png"
        )
        screenshot.save(filename)
        print(f"Screenshot saved as {filename}")
        return json.dumps({"filename": filename})

    @staticmethod
    def delete_screenshot(arguments=None):
        if not os.path.exists(Config.ARCHIVE_DIR):
            os.mkdir(Config.ARCHIVE_DIR)

        for filename in os.listdir(Config.SCREENSHOT_DIR):
            file_path = os.path.join(Config.SCREENSHOT_DIR, filename)
            if os.path.isfile(file_path):
                new_path = os.path.join(Config.ARCHIVE_DIR, filename)
                os.rename(file_path, new_path)

        return json.dumps({"status": "Screenshots moved to archive"})
