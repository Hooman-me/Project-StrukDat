@echo off
REM 
if exist "C:\MSYS2\mingw64\bin\python.exe" (
    "C:\MSYS2\mingw64\bin\python.exe" app.py
) else (
    python app.py
)
pause
