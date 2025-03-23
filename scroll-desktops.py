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
import sys
import argparse

#################### Windows-specific shortcuts ##############################

def windows_desktop_overview() -> None:
    """
    Shows the desktop overview on Windows 10/11.
    """
    keyboard.press(Key.cmd)
    keyboard.press(Key.tab)
    keyboard.release(Key.cmd)
    keyboard.release(Key.tab)


def windows_switch_desktops(direction: str) -> None:
    """
    Switches between virtual desktops on Windows 10/11.

    Args:
        direction (str): The direction to switch desktops. Can be 'right' or 'left'.
    """
    keyboard.press(Key.cmd)
    keyboard.press(Key.ctrl)
    if direction == 'right':
        keyboard.press(Key.right)
    else:
        keyboard.press(Key.left)

    keyboard.release(Key.cmd)
    keyboard.release(Key.ctrl)
    if direction == 'right': 
        keyboard.release(Key.right)
    else:
        keyboard.release(Key.left)

#################### macOS-specific shortcuts ################################

def mac_switch_desktops(direction: str) -> None:
    """
    Switches between virtual desktops on macOS.

    Args:
        direction (str): The direction to switch desktops. Can be 'right' or 'left'.
    """
    if direction == 'right':
        keyboard.press(Key.ctrl)
        keyboard.press(Key.right)
        keyboard.release(Key.ctrl)
        keyboard.release(Key.right)
    else:
        keyboard.press(Key.ctrl)
        keyboard.press(Key.left)
        keyboard.release(Key.ctrl)
        keyboard.release(Key.left)


def mac_desktop_overview() -> None:
    """
    Shows the desktop overview on macOS.
    """
    keyboard.press(Key.ctrl)
    keyboard.press(Key.up)
    keyboard.release(Key.ctrl)
    keyboard.release(Key.up)

################## Create all trigger zones ##################################

def get_trigger_area(monitor: screeninfo.common.Monitor, vertical_margin: int = 1) -> list:
    """
    Get the trigger area for switching desktops.

    Args:
        monitor (screeninfo.common.Monitor): The monitor object.
        vertical_margin (int): The vertical margin for the trigger area. Default 1 pixel.

    Returns:
        list: The coordinates of the trigger area [x_left, y_left, x_right, y_right].
    """
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

######################### Event handlers #####################################

def on_scroll(x: int, y: int, dx: int, dy: int, scroll_delay: float = 0.1, repeat_delay: float = 0.2) -> None:
    """
    Handles mouse scroll events for switching desktops based on the scroll direction and position.

    This function checks whether the scroll event occurs within any defined monitor regions.
    If so, it determines the desired desktop switch direction based on the vertical scroll delta (dy).
    A desktop switch is triggered if sufficient time has elapsed since the last scroll (as per scroll_delay)
    or if a repeated scroll in the same direction occurs after the repeat_delay.

    Args:
        x (int): The x-coordinate of the mouse at the time of the scroll event.
        y (int): The y-coordinate of the mouse at the time of the scroll event.
        dx (int): The horizontal component of the scroll delta.
        dy (int): The vertical component of the scroll delta.
        scroll_delay (float, optional): The minimum delay between processing consecutive scroll events.
                                        Default is 0.1.
        repeat_delay (float, optional): The additional delay required before processing a repeated scroll event
                                        in the same direction. Default is 0.2.

    Returns:
        None

    Side Effects:
        Updates the global variables 'last_scroll_time' and 'last_move' and calls 'switch_desktops(move)'
        to switch desktops based on the computed direction.
    """

    global last_scroll_time
    global last_move
    current_time = time.time()

    # If the time since the last scroll is greater than the delay
    delta_t = current_time - last_scroll_time
    if delta_t >= scroll_delay:
        # If the mouse is within the bounds of the trigger area
        if any(is_point_inside_rectangle((x, y), monitor) for monitor in monitors):
            move = 'right' if dy < 0 else 'left'
            if last_move != move or delta_t >= repeat_delay:
                switch_desktops(move)
                last_move = move

        last_scroll_time = current_time


def on_move(x: int, y: int, delay: float = 0.5) -> None:
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
        if current_time - last_hot_corner_time >= delay:
            # Press shortcut to show desktop overview
            desktop_overview()

        last_hot_corner_time = current_time

####################### Main script ###########################################

if __name__ == '__main__':

    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Switch virtual desktops using mouse scroll and a hot corner."
    )
    parser.add_argument(
        "--scroll_delay",
        type=float,
        default=0.1,
        help="Minimum delay between processing consecutive scroll events (default: 0.1 seconds).",
    )
    parser.add_argument(
        "--repeat_delay",
        type=float,
        default=0.2,
        help="Additional delay for repeated scroll events in the same direction (default: 0.2 seconds).",
    )
    parser.add_argument(
        "--hot_corner_delay",
        type=float,
        default=0.5,
        help="Delay for triggering the hot corner action (default: 0.5 seconds).",
    )
    args = parser.parse_args()

    # Override the on_scroll function to include the scroll_delay and repeat_delay arguments
    _original_on_scroll = on_scroll
    def on_scroll(x, y, dx, dy):
        _original_on_scroll(x, y, dx, dy, scroll_delay=args.scroll_delay, 
                            repeat_delay=args.repeat_delay)
        
    # Override the on_move function to include the hot_corner_delay argument
    _original_on_move = on_move
    def on_move(x, y):
        _original_on_move(x, y, delay=args.hot_corner_delay)

    # Initialize global variables
    last_scroll_time = time.time()
    last_hot_corner_time = time.time()
    last_move = None

    # Determine the OS and set the appropriate shortcuts
    platform_system = sys.platform
    if platform_system == 'win32':
        # Windows-specific functions
        switch_desktops = windows_switch_desktops
        desktop_overview = windows_desktop_overview
    elif platform_system == 'darwin':
        # Mac-specific functions
        switch_desktops = mac_switch_desktops
        desktop_overview = mac_desktop_overview
    else:
        print("Unsupported OS")
        sys.exit(1)

    # Get the trigger areas for each monitor
    monitors = [get_trigger_area(monitor) for monitor in get_monitors()]
    print("Monitors: ", len(monitors))

    # Initialize the keyboard controller
    keyboard = Controller()

    # Event loop: listener for mouse scroll and move events
    with mouse.Listener(on_scroll=on_scroll, on_move=on_move) as listener:
        listener.join()
