@echo off
REM Script peluncur aplikasi 2EZ4U Food Delivery
if exist "C:\MSYS2\mingw64\bin\python.exe" (
    "C:\MSYS2\mingw64\bin\python.exe" app.py
) else (
    python app.py
)
pause
