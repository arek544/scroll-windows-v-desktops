from pynput import mouse
from pynput.keyboard import Key, Controller
import json
import time

with open('config.json', 'r') as f:
  config = json.load(f)

keyboard = Controller()
last_scroll_time = time.time()

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
