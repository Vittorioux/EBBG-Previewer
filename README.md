# EBBG-Previewer
Simple Tkinter application for previewing EarthBound battle backgrounds with an emulator.

## How to use
- Run the program from source or build the .EXE.
- Load a ROM, it has to be either a clean ROM or a ROM modified by this program only.
- Load 2BPP or 4BPP PNGs as the battle backgrounds to preview.
- Visit the different tabs to set palette cycling, scrolling and distortion settings.
- You can also load full settings from a vanilla BG by using the 'Load entry' button.
- Click "Execute" so all the data is written into the ROM.
- Click "Run" to open the modified ROM with an emulator (specify the path to the emulator in the corresponding field).
- Hold Y in-game to pause the animation.
- Press L in-game to change the letterbox size.
- To get the settings in the proper CoilSnake YML's format click the 'YML Format' button and copy the parts you need.

## Dependencies
This program uses Inhal by devinacker and SuperFamiconV by Optiroc (so big thanks to them!).

- [Inhal/Exhal](https://github.com/devinacker/exhal)
- [SuperFamiconV](https://github.com/Optiroc/SuperFamiconv)

## How to run from source
- Create a Python venv and run the activation script.
- Install Pillow (Pyinstaller is not required).
- Run `ui.py` with Python.

## How to build
- Create a Python venv and run the activation script.
- Install requirements (found in requirements.txt).
- Run the following command:
```
$ pyinstaller --onefile --name "EBBG Previewer" --noconsole --icon=assets\icon.ico --add-binary="assets\icon.ico;." --add-binary="assets\superfamiconv.exe;." --add-binary="assets\inhal.exe;." src/ui.py
```
Alternatively, run `windows_make_exe.bat`, which performs exactly these steps.