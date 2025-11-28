@echo off
REM ===================================================================
REM  HIRING AUTOMATION - SEND NOTIFICATIONS
REM  Double-click this file to send emails and WhatsApp messages
REM ===================================================================

echo.
echo ============================================================
echo   HIRING AUTOMATION - SEND NOTIFICATIONS
echo ============================================================
echo.
echo This will:
echo  1. Read approved candidates from Google Sheets
echo  2. Send personalized emails (Gmail API)
echo  3. Send personalized WhatsApp messages (Twilio)
echo.
echo IMPORTANT: Make sure you have:
echo  - Marked candidates as "Yes" in the hr_approved column
echo  - Set up Gmail API credentials (optional)
echo  - Set up Twilio credentials (optional)
echo.
echo Press any key to continue or close this window to cancel...
pause > nul

echo.
echo Starting notification process...
echo.

python send_notifications.py

echo.
echo ============================================================
echo   Process Complete!
echo ============================================================
echo.
echo Press any key to close this window...
pause > nul
