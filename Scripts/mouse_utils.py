import pyautogui
import json

def parse_arguments(func):
    def wrapper(cls, arguments=None):
        try:
            args = json.loads(arguments) if isinstance(arguments, str) else arguments or {}
            result = func(cls, args)
            return json.dumps(result)
        except Exception as e:
            return json.dumps({"error": str(e)})
    return wrapper

class MouseUtils:
    FAILSAFE = True
    pyautogui.FAILSAFE = FAILSAFE
    SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()

    @classmethod
    @parse_arguments
    def move_mouse_to(cls, args):
        x = args.get('x')
        y = args.get('y')
        duration = args.get('duration', 0.5)
        if x is None or y is None:
            return {"error": "Missing x or y coordinates"}
        x = min(max(0, x), cls.SCREEN_WIDTH)
        y = min(max(0, y), cls.SCREEN_HEIGHT)
        pyautogui.moveTo(x, y, duration=duration)
        return {
            "status": "success",
            "x": x,
            "y": y,
            "duration": duration,
            "screen_width": cls.SCREEN_WIDTH,
            "screen_height": cls.SCREEN_HEIGHT
        }

    @classmethod
    @parse_arguments
    def move_mouse_relative(cls, args):
        x_offset = args.get('x_offset')
        y_offset = args.get('y_offset')
        duration = args.get('duration', 0.5)
        if x_offset is None or y_offset is None:
            return {"error": "Missing x_offset or y_offset"}
        curr_x, curr_y = pyautogui.position()
        new_x = min(max(0, curr_x + x_offset), cls.SCREEN_WIDTH)
        new_y = min(max(0, curr_y + y_offset), cls.SCREEN_HEIGHT)
        actual_x_offset = new_x - curr_x
        actual_y_offset = new_y - curr_y
        pyautogui.moveRel(actual_x_offset, actual_y_offset, duration=duration)
        return {
            "status": "success", 
            "x_offset": actual_x_offset,
            "y_offset": actual_y_offset,
            "duration": duration,
            "screen_width": cls.SCREEN_WIDTH,
            "screen_height": cls.SCREEN_HEIGHT
        }

    @classmethod
    @parse_arguments
    def get_mouse_position(cls, args=None):
        pos = pyautogui.position()
        return {"status": "success", "x": pos.x, "y": pos.y}

    @classmethod
    @parse_arguments
    def click(cls, args=None):
        x = args.get('x')
        y = args.get('y')
        if x is not None and y is not None:
            pyautogui.click(x, y)
            return {"status": "success", "x": x, "y": y}
        pyautogui.click()
        pos = pyautogui.position()
        return {"status": "success", "x": pos.x, "y": pos.y}

    @classmethod
    @parse_arguments
    def double_click(cls, args=None):
        x = args.get('x')
        y = args.get('y')
        if x is not None and y is not None:
            pyautogui.doubleClick(x, y)
            return {"status": "success", "x": x, "y": y}
        pyautogui.doubleClick()
        pos = pyautogui.position()
        return {"status": "success", "x": pos.x, "y": pos.y}
