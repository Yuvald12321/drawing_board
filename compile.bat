pyinstaller --noconsole --onefile --icon=logo.ico -n "drawing board" main.py
rd /S /Q "build"
del /Q "drawing board.spec"
