@echo off
echo Testing FastAPI Year Logic...
echo.

echo Testing 2022 (should be historical=true):
curl -X GET "http://localhost:8000/test/year/2022"
echo.
echo.

echo Testing 2024 (should be historical=true):
curl -X GET "http://localhost:8000/test/year/2024"
echo.
echo.

echo Testing 2025 (should be historical=false):
curl -X GET "http://localhost:8000/test/year/2025"
echo.
echo.

echo Testing full prediction for 2022:
curl -X POST "http://localhost:8000/predict" -H "Content-Type: application/json" -d "{\"season\": 2022, \"team_encoded\": 0, \"driver_name\": \"Sergio Perez\", \"race_name\": \"Italian Grand Prix\"}"
echo.
echo.

pause
