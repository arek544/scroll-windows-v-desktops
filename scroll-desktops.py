from pynput import mouse
from pynput.keyboard import Key, Controller
import json
import time

with open('config.json', 'r') as f:
  config = json.load(f)

keyboard = Controller()
last_scroll_time = time.time()
last_hot_corner_time = time.time()

def on_scroll(x, y, dx, dy):
  global last_scroll_time
  current_time = time.time()
  if current_time - last_scroll_time >= config['scroll_delay']:
    if (
      x >= config['xMin'] and 
      x <= config['xMax'] and 
      y >= config['yMin'] and 
      y <= config['yMax']
    ):
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
      
    if config['printPosition']:
      print('Scrolled {0} at {1}'.format(
        'down' if dy < 0 else 'up',
        (x, y)))
      
    last_scroll_time = current_time

def on_move(x, y):
  global last_hot_corner_time
  current_time = time.time()
  if (
      x >= config['xMin'] and 
      x <= config['xMin'] + 1 and 
      y >= config['yMin'] and 
      y <= config['yMin'] + 1
  ):

    delay = 0.5
    if current_time - last_hot_corner_time >= delay:
      keyboard.press(Key.cmd)
      keyboard.press(Key.tab)
      keyboard.release(Key.cmd)
      keyboard.release(Key.tab)

    last_hot_corner_time = current_time

if config['hotCorner']:
  # Switch desktops with scroll wheel and show overview when mouse is 
  # in upper-left corner of main desktop so called "hot corner"
  with mouse.Listener(on_scroll=on_scroll, on_move=on_move) as listener:
    listener.join()
else:
  # Only switch desktops with scroll wheel
  with mouse.Listener(on_scroll=on_scroll) as listener:
    listener.join()