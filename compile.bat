call ".venv\Scripts\pyinstaller.exe" --onefile --noconsole --icon "logo.ico" -n "drawing board" main.py
rd /S /Q "build"