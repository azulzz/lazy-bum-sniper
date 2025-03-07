@echo off
cls

if not exist ".venv\" (
    echo Creating virtual environment...
    python -m venv .venv
) else (
    goto skip_install
)

call .venv\Scripts\activate.bat

echo Starting installation process...

cls
echo Installing (1/7) Packages
python -m pip install -U git+https://github.com/dolfies/discord.py-self

cls
echo Installing (2/7) Packages
python -m pip install requests

cls
echo Installing (3/7) Packages
python -m pip install pyautoit

cls
echo Installing (4/7) Packages
python -m pip install ttkthemes

cls
echo Installing (5/7) Packages
python -m pip install pure-python-adb

cls
echo Installing (6/7) Packages
python -m pip install discord-webhook

cls
echo Installing (7/7) Packages
python -m pip install bs4

cls
echo Installation completed!

:skip_install
call sniper.bat

exit