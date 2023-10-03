@echo off
setlocal

if "%~5"=="" (
    echo Usage: %~nx0 [path] [year] [month] [day] [account]
    exit /b 1
)

"%1\gallery-dl.exe" https://twitter.com/%5/ --filter "date >= datetime(%2, %3, %4) or abort()"

endlocal