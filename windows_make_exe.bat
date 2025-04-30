@echo off
setlocal

python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python wasn't detected or not in PATH.
    pause
    exit /b 1
)

for /f "delims=" %%i in ('python --version') do set PYVER=%%i
echo Python version detected: %PYVER%
echo.

REM ------------------------------
REM EBBG Previewer Windows builder
REM ------------------------------

if not exist venv\Scripts\activate (
	echo Creating venv...
	echo.
	
	python -m venv venv
	call venv\Scripts\activate
	
	echo Upgrading pip...
	echo.
	
	python -m pip install --upgrade pip
	
	echo.
	echo Installing requirements...
	echo.
	
	pip install -r requirements.txt
	echo.
)

echo Activating venv...

call venv\Scripts\activate

echo.
echo Compiling...
echo.

pyinstaller --onefile --name "EBBG Previewer" --noconsole --icon=assets\icon.ico --add-binary="assets\icon.ico;." --add-binary="assets\superfamiconv.exe;." --add-binary="assets\inhal.exe;." src/ui.py

rmdir /s /q build
del *.spec

echo.
echo Compilation complete!
echo Find the .EXE in /dist/
echo.

pause