@echo off
echo Starting F1 Prediction Services...

echo.
echo Starting FastAPI service...
cd /d "c:\Users\uzair\Desktop\Dev\Spring\F1\New folder\Analysis"
start "FastAPI" cmd /k "python -m uvicorn main:app --reload --port 8000"

echo.
echo Waiting 5 seconds for FastAPI to start...
timeout /t 5 /nobreak

echo.
echo Starting Spring Boot service...
cd /d "c:\Users\uzair\Desktop\Dev\Spring\F1\New folder\demo\demo"
start "Spring Boot" cmd /k "mvn spring-boot:run"

echo.
echo Both services are starting...
echo FastAPI will be available at: http://localhost:8000
echo Spring Boot will be available at: http://localhost:8080
echo Frontend should connect to: http://localhost:8080/api/predict

pause
