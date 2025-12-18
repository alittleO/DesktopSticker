@echo off
cd /d "%~dp0"

if not exist "main.py" (
    echo Error: main.py not found!
    pause
    exit
)

REM 使用检测到的绝对路径
set "PYTHON_PATH=C:\ProgramData\miniconda3\pythonw.exe"

if exist "%PYTHON_PATH%" (
    start "" "%PYTHON_PATH%" "main.py"
) else (
    REM 如果找不到绝对路径，尝试直接调用 pythonw
    start "" pythonw "main.py"
)
