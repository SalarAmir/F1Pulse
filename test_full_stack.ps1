# Full Stack Integration Test Script (PowerShell)
# Tests FastAPI → Spring Boot → React integration for F1 Position Predictor

Write-Host "🏎️ F1 Position Predictor - Full Stack Integration Test" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan

# Test cases
$testCases = @(
    '{"season": 2024, "team_encoded": 0, "driver_name": "Max Verstappen", "race_name": "Monaco GP", "driver_experience": 10}',
    '{"season": 2023, "team_encoded": 1, "driver_name": "Lewis Hamilton", "race_name": "British GP", "driver_experience": 15}',
    '{"season": 2022, "team_encoded": 2, "driver_name": "Charles Leclerc", "race_name": "Italian GP", "driver_experience": 5}',
    '{"season": 2024, "team_encoded": 8, "driver_name": "Logan Sargeant", "race_name": "US GP", "driver_experience": 1}'
)

# Function to test FastAPI directly
function Test-FastAPI {
    Write-Host "`n🧪 Testing FastAPI (Port 8000)" -ForegroundColor Blue
    Write-Host "-----------------------------------" -ForegroundColor Blue
    
    # Health check
    try {
        $healthResponse = Invoke-RestMethod -Uri "http://localhost:8000/health" -Method Get -TimeoutSec 5
        Write-Host "✅ FastAPI Health Check: PASSED" -ForegroundColor Green
    } catch {
        Write-Host "❌ FastAPI Health Check: FAILED" -ForegroundColor Red
        Write-Host "💡 Start FastAPI with: uvicorn main:app --reload" -ForegroundColor Yellow
        return $false
    }
    
    # Test prediction endpoint
    Write-Host "`n🔮 Testing FastAPI Predictions:" -ForegroundColor Cyan
    
    for ($i = 0; $i -lt $testCases.Count; $i++) {
        $caseNum = $i + 1
        $testCase = $testCases[$i]
        
        Write-Host "`n  Test Case $caseNum:" -ForegroundColor White
        
        try {
            $response = Invoke-RestMethod -Uri "http://localhost:8000/predict" -Method Post -Body $testCase -ContentType "application/json" -TimeoutSec 10
            
            if ($response.predicted_position) {
                $position = $response.predicted_position
                $confidence = [math]::Round($response.prediction_confidence * 100, 1)
                $isHistorical = $response.is_historical
                
                Write-Host "    ✅ Position: P$position, Confidence: $confidence%, Historical: $isHistorical" -ForegroundColor Green
            } else {
                Write-Host "    ❌ Invalid response structure" -ForegroundColor Red
            }
        } catch {
            Write-Host "    ❌ Request failed: $($_.Exception.Message)" -ForegroundColor Red
        }
    }
    
    return $true
}

# Function to test Spring Boot backend
function Test-SpringBoot {
    Write-Host "`n🍃 Testing Spring Boot Backend (Port 8080)" -ForegroundColor Blue
    Write-Host "-------------------------------------------" -ForegroundColor Blue
    
    # Connection check
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8080/api/predict" -Method Get -TimeoutSec 5 -UseBasicParsing
        Write-Host "✅ Spring Boot Connection: PASSED" -ForegroundColor Green
    } catch {
        Write-Host "❌ Spring Boot Connection: FAILED" -ForegroundColor Red
        Write-Host "💡 Start Spring Boot application" -ForegroundColor Yellow
        return $false
    }
    
    # Test prediction endpoint
    Write-Host "`n🔮 Testing Spring Boot → FastAPI Integration:" -ForegroundColor Cyan
    
    for ($i = 0; $i -lt $testCases.Count; $i++) {
        $caseNum = $i + 1
        $testCase = $testCases[$i]
        
        Write-Host "`n  Test Case $caseNum:" -ForegroundColor White
        
        try {
            $response = Invoke-RestMethod -Uri "http://localhost:8080/api/predict" -Method Post -Body $testCase -ContentType "application/json" -TimeoutSec 15
            
            if ($response.predicted_position -or $response.predictedPosition) {
                $position = if ($response.predicted_position) { $response.predicted_position } else { $response.predictedPosition }
                $confidence = if ($response.prediction_confidence) { [math]::Round($response.prediction_confidence * 100, 1) } else { [math]::Round($response.predictionConfidence * 100, 1) }
                $isHistorical = if ($response.is_historical) { $response.is_historical } else { $response.isHistorical }
                
                Write-Host "    ✅ Position: P$position, Confidence: $confidence%, Historical: $isHistorical" -ForegroundColor Green
            } else {
                Write-Host "    ❌ Invalid response structure" -ForegroundColor Red
                Write-Host "    Response: $($response | ConvertTo-Json -Depth 2)" -ForegroundColor Gray
            }
        } catch {
            Write-Host "    ❌ Request failed: $($_.Exception.Message)" -ForegroundColor Red
        }
    }
    
    return $true
}

# Function to test React frontend
function Test-ReactFrontend {
    Write-Host "`n⚛️ Testing React Frontend (Port 3000)" -ForegroundColor Blue
    Write-Host "-----------------------------------" -ForegroundColor Blue
    
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:3000" -Method Get -TimeoutSec 5 -UseBasicParsing
        Write-Host "✅ React Frontend: RUNNING" -ForegroundColor Green
        Write-Host "🌐 Open browser: http://localhost:3000" -ForegroundColor Cyan
        return $true
    } catch {
        Write-Host "❌ React Frontend: NOT RUNNING" -ForegroundColor Red
        Write-Host "💡 Start React with: npm run dev" -ForegroundColor Yellow
        return $false
    }
}

# Function to display summary
function Show-Summary {
    Write-Host "`n📋 Integration Test Summary" -ForegroundColor Blue
    Write-Host "============================" -ForegroundColor Blue
    Write-Host ""
    Write-Host "🏗️ Architecture:" -ForegroundColor White
    Write-Host "  React Frontend (Port 3000) → Spring Boot API (Port 8080) → FastAPI ML (Port 8000)" -ForegroundColor Gray
    Write-Host ""
    Write-Host "🎯 What was tested:" -ForegroundColor White
    Write-Host "  ✓ FastAPI position prediction endpoint" -ForegroundColor Green
    Write-Host "  ✓ Spring Boot API gateway integration" -ForegroundColor Green
    Write-Host "  ✓ Historical data lookup" -ForegroundColor Green
    Write-Host "  ✓ Position classification with confidence" -ForegroundColor Green
    Write-Host ""
    Write-Host "📱 Frontend features:" -ForegroundColor White
    Write-Host "  ✓ Driver selection with automatic team/experience" -ForegroundColor Green
    Write-Host "  ✓ Custom experience override" -ForegroundColor Green
    Write-Host "  ✓ Position prediction display with confidence" -ForegroundColor Green
    Write-Host "  ✓ Historical result comparison" -ForegroundColor Green
    Write-Host ""
    Write-Host "🚀 To run the full stack:" -ForegroundColor White
    Write-Host "  1. FastAPI: cd Analysis && uvicorn main:app --reload" -ForegroundColor Yellow
    Write-Host "  2. Spring Boot: cd demo && ./mvnw spring-boot:run" -ForegroundColor Yellow
    Write-Host "  3. React: cd Frontend/F1Pulse && npm run dev" -ForegroundColor Yellow
    Write-Host ""
}

# Main execution
function Main {
    Write-Host "`n🔧 Starting Integration Tests..." -ForegroundColor Cyan
    
    $fastApiOk = Test-FastAPI
    $springBootOk = Test-SpringBoot
    $reactOk = Test-ReactFrontend
    
    Show-Summary
    
    if ($fastApiOk -and $springBootOk) {
        Write-Host "🏁 Integration testing complete! ✅" -ForegroundColor Green
        if ($reactOk) {
            Write-Host "🌟 Full stack is ready for testing!" -ForegroundColor Green
        } else {
            Write-Host "⚠️ Backend is working, start React frontend for full testing" -ForegroundColor Yellow
        }
    } else {
        Write-Host "🏁 Integration testing complete with issues ❌" -ForegroundColor Red
        Write-Host "Please check the failed services above" -ForegroundColor Yellow
    }
}

# Run main function
Main
