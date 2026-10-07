@echo off
title MediFlow - Online Appointment Booking System (ITL Lab & Scrum PBL)
color 0b
echo ===============================================================================
echo   🏥 MEDIFLOW : ONLINE APPOINTMENT BOOKING SYSTEM
echo   B.Tech 3rd Year Agile Methodology PBL / ITL Lab Project
echo ===============================================================================
echo.
echo Starting MediFlow Web Server and Dashboard...
echo Database: SQLite (database/appointment.db)
echo Concurrency Guard: Atomic Transactions Enabled
echo.

where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Python is not found in system PATH!
    echo Please install Python 3.10+ from python.org and tick 'Add Python to PATH'.
    pause
    exit /b 1
)

python app.py

if %ERRORLEVEL% neq 0 (
    echo.
    echo Server exited with an error. Press any key to close.
    pause
)
