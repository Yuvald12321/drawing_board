@echo off
setlocal enabledelayedexpansion

set "REG_KEY=HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders"
set "RAW_PATH="

for /f "tokens=2,*" %%A in ('reg query "%REG_KEY%" /v "{758026A1-9253-400D-A76F-15E2157B228D}" 2^>nul') do (
    set "RAW_PATH=%%B"
)

if not defined RAW_PATH (
    for /f "tokens=2,*" %%A in ('reg query "%REG_KEY%" /v "Desktop" 2^>nul') do (
        set "RAW_PATH=%%B"
    )
)

if defined RAW_PATH (
    call set "DESKTOP_PATH=%RAW_PATH%"
) else (
    set "DESKTOP_PATH=%USERPROFILE%\Desktop"
)

set "URL=https://raw.githubusercontent.com/Yuvald12321/drawing_board/master/dist/drawing%%20board.exe"
set "TARGET_FILE=%DESKTOP_PATH%\drawing board.exe"

echo Downloading to: "%TARGET_FILE%"
curl -L -s -f -o "%TARGET_FILE%" "%URL%"

if %ERRORLEVEL% equ 0 (
    echo Successfully downloaded drawing board.exe to Desktop!
    timeout /t 5
    start "" "%TARGET_FILE%"
) else (
    echo Error: Failed to download the file.
    pause
)