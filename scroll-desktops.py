"""
This script allows you to switch between virtual desktops on Windows 10/11 
using mouse scroll and hot corner.

Requirements:
- pynput library (install using pip install pynput)
- screeninfo library (install using pip install screeninfo)

Usage:
1. Run the script.
2. Move your cursor to the top of the screen and scroll the mouse wheel up 
   or down to switch between virtual desktops.
3. Move the mouse to the upper-left corner of the screen to show the desktop
   overview.

Note: This script is specifically designed for Windows 10/11.
"""

from pynput import mouse
from pynput.keyboard import Key, Controller
import time
from screeninfo import get_monitors
import screeninfo

#################### Windows-specific shortcuts ##############################


def winows_desktop_overview() -> None:
    """
    Shows the desktop overview on Windows 10.
    """
    keyboard.press(Key.cmd)
    keyboard.press(Key.tab)
    keyboard.release(Key.cmd)
    keyboard.release(Key.tab)


def windows_switch_desktops(dy: int) -> None:
    """
    Switches desktops on Windows 10.

    Args:
      dy (int): The vertical distance scrolled.
    """
    keyboard.press(Key.cmd)
    keyboard.press(Key.ctrl)
    if dy < 0:
        keyboard.press(Key.right)
    else:
        keyboard.press(Key.left)

    keyboard.release(Key.cmd)
    keyboard.release(Key.ctrl)
    if dy < 0:
        keyboard.release(Key.right)
    else:
        keyboard.release(Key.left)


################## Create all trigger zones ##################################


def get_trigger_area(monitor: screeninfo.common.Monitor) -> list:
    vertical_margin = 30
    return [
        monitor.x,
        monitor.y,
        monitor.x + monitor.width,
        monitor.y + vertical_margin,
    ]


def is_point_inside_rectangle(point: list, rectangle: list) -> bool:
    """
    Check if a point is inside a rectangle.

    Args:
        point (tuple): The coordinates of the point (x, y).
        rectangle (list): The coordinates of the rectangle
            [x_left_lower, y_left_lower, x_right_upper, y_right_upper].

    Returns:
        bool: True if the point is inside the rectangle, False otherwise.
    """
    x, y = point
    x_left_lower, y_left_lower, x_right_upper, y_right_upper = rectangle

    if (
        x_left_lower <= x <= x_right_upper
        and y_left_lower <= y <= y_right_upper
    ):
        return True
    else:
        return False


############################ Initialization ##################################

monitors = [get_trigger_area(monitor) for monitor in get_monitors()]
print("Monitors: ", len(monitors))

keyboard = Controller()
last_scroll_time = time.time()
last_hot_corner_time = time.time()
last_esc_press_time = time.time()


######################### Event handlers #####################################


def on_scroll(x: int, y: int, dx: int, dy: int) -> None:
    """
    Event handler for mouse scroll events.

    Args:
      x (int): The x-coordinate of the mouse cursor.
      y (int): The y-coordinate of the mouse cursor.
      dx (int): The horizontal distance scrolled.
      dy (int): The vertical distance scrolled.
    """

    global last_scroll_time
    current_time = time.time()
    scroll_delay = 0.3

    # If the time since the last scroll is greater than the delay
    if current_time - last_scroll_time >= scroll_delay:
        # If the mouse is within the bounds of the trigger area
        if any(
            [
                is_point_inside_rectangle((x, y), monitor)
                for monitor in monitors
            ]
        ):
            # Press shortcut to switch desktops
            windows_switch_desktops(dy)

        last_scroll_time = current_time


def on_move(x: int, y: int) -> None:
    """
    Callback function triggered when the mouse moves.

    Args:
      x (int): The x-coordinate of the mouse cursor.
      y (int): The y-coordinate of the mouse cursor.
    """

    global last_hot_corner_time
    current_time = time.time()

    # If the mouse is in the upper-left corner of the screen
    if x >= 0 and x <= 1 and y >= 0 and y <= 1:
        delay = 0.5
        if current_time - last_hot_corner_time >= delay:
            # Press shortcut to show desktop overview
            winows_desktop_overview()

        last_hot_corner_time = current_time


######################### Event loop ##########################################

with mouse.Listener(on_scroll=on_scroll, on_move=on_move) as listener:
    listener.join()
