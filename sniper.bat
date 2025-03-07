@echo off

if not exist ".venv\" (
    echo Running installer.bat
    call installer.bat
    exit
)

echo Starting the sniper!!
start .venv\Scripts\pythonw.exe lib/sniper.py
exit