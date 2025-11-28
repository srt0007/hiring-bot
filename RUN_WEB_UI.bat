@echo off
REM ===================================================================
REM  HIRING AUTOMATION - WEB UI
REM  Double-click this file to launch the web interface
REM ===================================================================

echo.
echo ============================================================
echo   HIRING AUTOMATION - WEB INTERFACE
echo ============================================================
echo.
echo Starting web server...
echo Your browser will open automatically at http://localhost:8501
echo.
echo To stop the server, close this window or press Ctrl+C
echo.
echo ============================================================
echo.

REM Install web dependencies if needed
echo Checking dependencies...
python -m pip install streamlit pandas --quiet

echo.
echo Launching web interface...
echo.

REM Start Streamlit
streamlit run app.py

pause
