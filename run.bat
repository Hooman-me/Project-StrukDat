@echo off
setlocal enabledelayedexpansion

REM Pindah ke direktori tempat skrip ini berada
cd /d "%~dp0"
title 2EZ4U Food Delivery - Launcher

echo ===================================================
echo     2EZ4U Food Delivery - Mini Engine Backend
echo ===================================================
echo.

REM 1. Periksa ketersediaan perintah python
set "PYTHON_EXE="

where python >nul 2>nul
if %ERRORLEVEL% equ 0 (
    set "PYTHON_EXE=python"
    goto :jalankan
)

REM 2. Cek path MSYS2 mingw64
if exist "C:\MSYS2\mingw64\bin\python.exe" (
    set "PYTHON_EXE=C:\MSYS2\mingw64\bin\python.exe"
    goto :jalankan
)

REM 3. Cek python launcher bawaan Windows (py)
where py >nul 2>nul
if %ERRORLEVEL% equ 0 (
    set "PYTHON_EXE=py"
    goto :jalankan
)

:jalankan
if "%PYTHON_EXE%"=="" (
    echo [ERROR] Python tidak ditemukan pada sistem ini!
    echo Silakan pastikan Python 3.11+ telah terpasang dan dicentang 'Add to PATH'.
    echo.
    pause
    exit /b 1
)

echo Menggunakan Python: %PYTHON_EXE%
echo Menjalankan aplikasi...
echo.

"%PYTHON_EXE%" app.py

if %ERRORLEVEL% neq 0 (
    echo.
    echo [PERINGATAN] Aplikasi ditutup dengan kode keluar %ERRORLEVEL%.
)

echo.
pause
