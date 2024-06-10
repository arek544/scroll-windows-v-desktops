"""
SIMPLIFIED VERSION OF THE SCRIPT - ONLY SINGLE PRIMARY MONITOR SUPPORTED

This script allows you to switch desktops by scrolling the mouse wheel while the cursor is in 
the top of the screen, and show the desktop overview by moving the cursor to the upper-left 
corner of the screen.
"""
from pynput import mouse
from pynput.keyboard import Key, Controller
import time
from screeninfo import get_monitors


def get_monitor_with_cursor():
    """
    Returns the monitor where the cursor is currently located.

    Returns:
        The monitor object where the cursor is located, or None if the cursor is not within any monitor.
    """
    x, y = mouse.Controller().position
    for m in get_monitors():
        if m.x <= x < m.x + m.width and m.y <= y < m.y + m.height:
            return m
    return None


keyboard = Controller()
last_scroll_time = time.time()
last_hot_corner_time = time.time()
last_esc_press_time = time.time()
esc_press_count = 0
monitor = get_monitor_with_cursor()


def on_scroll(x, y, dx, dy):
    """
    Event handler for mouse scroll events.

    Args:
      x (int): The x-coordinate of the mouse cursor.
      y (int): The y-coordinate of the mouse cursor.
      dx (int): The horizontal distance scrolled.
      dy (int): The vertical distance scrolled.
    """

    global last_scroll_time
    global monitor
    current_time = time.time()
    y_max = 30
    scroll_delay = 0.4

    # print(x,y)
    # If the time since the last scroll is greater than the delay
    if current_time - last_scroll_time >= scroll_delay:
        # If the mouse is within the bounds of the trigger area
        if (
            x >= 0
            and x <= monitor.width
            and y >= 0
            and y <= y_max
        ):
            # Press shortcut to switch desktops
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

        last_scroll_time = current_time


def on_move(x, y):
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
            keyboard.press(Key.cmd)
            keyboard.press(Key.tab)
            keyboard.release(Key.cmd)
            keyboard.release(Key.tab)

        last_hot_corner_time = current_time


with mouse.Listener(on_scroll=on_scroll, on_move=on_move) as listener:
    listener.join()
