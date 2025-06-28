@echo off
echo Starting F1 Position Prediction API...
echo =====================================

cd /d "c:\Users\uzair\Desktop\Dev\Spring\F1\New folder\Analysis"

echo Current directory: %CD%
echo.

echo Starting FastAPI server...
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

pause
