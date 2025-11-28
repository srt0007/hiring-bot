@echo off
REM ===================================================================
REM  HIRING AUTOMATION - OPEN GOOGLE SHEET
REM  Double-click this file to open the candidates spreadsheet
REM ===================================================================

echo.
echo ============================================================
echo   HIRING AUTOMATION - OPEN GOOGLE SHEET
echo ============================================================
echo.
echo Opening your Hiring Automation spreadsheet in browser...
echo.

REM Open the Google Sheet in default browser
start https://docs.google.com/spreadsheets/d/1hqcD0b1fuYjyJab1oLu9y_4wTuvM1EeQeFdbHV3zJGE

echo.
echo ============================================================
echo   Google Sheet opened in your browser!
echo ============================================================
echo.
echo You can now:
echo  - Review candidate information
echo  - Change hr_approved from "No" to "Yes" to approve candidates
echo  - Add manual comments or notes
echo.
echo This window will close in 3 seconds...
timeout /t 3 > nul
