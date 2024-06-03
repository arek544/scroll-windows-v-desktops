# Scroll Windows Virtual Desktops

Scroll through your virtual desktops by using the mouse wheel when your cursor is at the upper edge of the screen, similar to the functionality provided by the Gnome extension [Desktop Scroller All Sides](https://extensions.gnome.org/extension/561/desktop-scroller-all-sides-for-gnome-36/).

To trigger the desktop overview, move your cursor to the upper left corner of the screen (Windows + Tab).

See https://medium.com/p/cbb659435849 for more details of original repo.

## Install requirements

```sh
pip install -r requirements.txt
```

## Build

```sh
pyinstaller --onefile scroll-desktops.py
```

Builded file is in `./dist`

If you get an `Import Error` while running the compiled exe try to use the following command:

```sh
pyinstaller --hidden-import "pynput.keyboard._win32" --hidden-import "pynput.mouse._win32" --onefile scroll-desktops.py
```

If you don't want to see a window when you open the exe add the following flags to the pyinstaller command:

```sh
--nowindowed --noconsole
```
