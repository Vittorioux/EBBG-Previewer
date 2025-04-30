# EBBG-Previewer
Tkinter application for previewing EarthBound battle backgrounds with an emulator.

## How to use
- 1. Load a ROM, it has to be either a clean ROM or a ROM modified by this program only.
- 2. Load 2BPP or 4BPP PNGs as the battle backgrounds to preview.
- 3. Visit the different tabs to set palette cycling, scrolling and distortion settings.
- 4. Click "Execute" so all the data is written into the ROM.
- 5. Click "Run" to open the modified ROM with an emulator (specify the path to the emulator in "Settings").

## Dependencies
This program uses Inhal by devinacker and SuperFamiconV by Optiroc (so big thanks to them!).

- [Inhal/Exhal](https://github.com/devinacker/exhal)
- [SuperFamiconV](https://github.com/Optiroc/SuperFamiconv)

## How to build
- 1. Create a Python venv and run the activation script.
- 2. Install requirements (found in requirements.txt).
- 3. Run the following command:
```
$ pyinstaller --onefile --name "EBBG Previewer" --noconsole --icon=assets\icon.ico --add-binary="assets\icon.ico;." --add-binary="assets\superfamiconv.exe;." --add-binary="assets\inhal.exe;." src/ui.py
```
Alternatively, run `windows_make_exe.bat`, which performs exactly these steps.