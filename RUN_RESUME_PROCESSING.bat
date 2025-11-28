@echo off
REM ===================================================================
REM  HIRING AUTOMATION - RESUME PROCESSING
REM  Double-click this file to process resumes automatically
REM ===================================================================

echo.
echo ============================================================
echo   HIRING AUTOMATION - RESUME PROCESSING
echo ============================================================
echo.
echo This will:
echo  1. Read resumes from the 'resumes' folder
echo  2. Match them against the job description
echo  3. Save results to Google Sheets
echo.
echo Press any key to continue or close this window to cancel...
pause > nul

echo.
echo Starting resume processing...
echo.

python ingest_resumes.py

echo.
echo ============================================================
echo   Process Complete!
echo ============================================================
echo.
echo Press any key to close this window...
pause > nul
