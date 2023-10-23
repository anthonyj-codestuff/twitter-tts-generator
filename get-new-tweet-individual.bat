@echo off
setlocal

if "%~3"=="" (
    echo Usage: %~nx0 [path] [account] [tweet_id]
    exit /b 1
)

"%1\gallery-dl.exe" https://twitter.com/%2/status/%3

endlocal