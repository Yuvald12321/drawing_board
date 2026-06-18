call ".venv\Scripts\pyinstaller.exe" --specpath "build" --onefile --noconsole --icon "logo.ico" -n "drawing board" main.py
rd /S /Q "build"