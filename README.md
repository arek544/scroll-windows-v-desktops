# Scroll Windows Virtual Desktops

This is a single-file program that does not require root privileges, only Python and two packages specified in the requirements.

Scroll through your virtual desktops by using the mouse wheel when your cursor is at the upper edge of the screen, similar to the functionality provided by the Gnome extension [Desktop Scroller All Sides](https://extensions.gnome.org/extension/561/desktop-scroller-all-sides-for-gnome-36/).

To trigger the desktop overview, move your cursor to the upper left corner of the screen (`Windows` + `Tab`).

See https://medium.com/p/cbb659435849 for more details of the original repo.

## Requirements

- Python (tested on 3.12)
- `pynput` library 
- `screeninfo` library 
- supported Windows 10/11, MacOS

## Quick guide

1. Setup environment.
1. Run the script `scroll-desktops.py`
2. Move your cursor to the top of the screen and scroll the mouse wheel up or down to switch between virtual desktops.
3. Move the mouse to the upper-left corner of the primary screen to show the desktop overview.

## Additional CLI arguments (Optional)

- `--scroll_delay`: Sets the minimum delay (in seconds) between processing consecutive scroll events.
- `--repeat_delay`: Sets an additional delay (in seconds) for repeated scroll events in the same direction.
- `--hot_corner_delay`: Sets the delay (in seconds) for triggering the hot corner action. Set higher to avoid accidental triggers.


## Install Requirements

```sh
pip install -r requirements.txt
```

## Run script

```sh
python scroll-desktop.py
```

## Build (Windows .exe)

```sh
pyinstaller --onefile scroll-desktops.py
```

The built file is in `./dist`.

If you get an `Import Error` while running the compiled exe, try using the following command:

```sh
pyinstaller --hidden-import "pynput.keyboard._win32" --hidden-import "pynput.mouse._win32" --onefile scroll-desktops.py
```

If you don't want to see a window when you open the exe, add the following flags to the pyinstaller command:

```sh
--nowindowed --noconsole
```
