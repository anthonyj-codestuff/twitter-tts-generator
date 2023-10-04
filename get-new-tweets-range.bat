@echo off
setlocal

if "%~8"=="" (
    echo Usage: %~nx0 [path] [startyear] [startmonth] [startday] [endyear] [endmonth] [endday] [account]
    exit /b 1
)

"%1\gallery-dl.exe" https://twitter.com/%8/ --filter "date >= datetime(%2, %3, %4) and date < datetime(%5, %6, %7) or abort()"

endlocal