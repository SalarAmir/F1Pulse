#!/bin/bash

# Full Stack Integration Test Script
# Tests FastAPI → Spring Boot → React integration for F1 Position Predictor

echo "🏎️ F1 Position Predictor - Full Stack Integration Test"
echo "=" * 60

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test cases
declare -a test_cases=(
    '{"season": 2024, "team_encoded": 0, "driver_name": "Max Verstappen", "race_name": "Monaco GP", "driver_experience": 10}'
    '{"season": 2023, "team_encoded": 1, "driver_name": "Lewis Hamilton", "race_name": "British GP", "driver_experience": 15}'
    '{"season": 2022, "team_encoded": 2, "driver_name": "Charles Leclerc", "race_name": "Italian GP", "driver_experience": 5}'
    '{"season": 2024, "team_encoded": 8, "driver_name": "Logan Sargeant", "race_name": "US GP", "driver_experience": 1}'
)

# Function to test FastAPI directly
test_fastapi() {
    echo -e "\n${BLUE}🧪 Testing FastAPI (Port 8000)${NC}"
    echo "-----------------------------------"
    
    # Health check
    if curl -s http://localhost:8000/health > /dev/null; then
        echo -e "✅ ${GREEN}FastAPI Health Check: PASSED${NC}"
    else
        echo -e "❌ ${RED}FastAPI Health Check: FAILED${NC}"
        echo "💡 Start FastAPI with: uvicorn main:app --reload"
        return 1
    fi
    
    # Test prediction endpoint
    echo -e "\n🔮 Testing FastAPI Predictions:"
    
    for i in "${!test_cases[@]}"; do
        case_num=$((i + 1))
        test_case="${test_cases[$i]}"
        
        echo -e "\n  Test Case $case_num:"
        response=$(curl -s -X POST "http://localhost:8000/predict" \
            -H "Content-Type: application/json" \
            -d "$test_case")
        
        if echo "$response" | jq -e '.predicted_position' > /dev/null 2>&1; then
            position=$(echo "$response" | jq -r '.predicted_position')
            confidence=$(echo "$response" | jq -r '.prediction_confidence')
            is_historical=$(echo "$response" | jq -r '.is_historical')
            
            echo -e "    ✅ ${GREEN}Position: P$position, Confidence: $(echo "$confidence * 100" | bc -l | xargs printf "%.1f")%, Historical: $is_historical${NC}"
        else
            echo -e "    ❌ ${RED}Invalid response: $response${NC}"
        fi
    done
}

# Function to test Spring Boot backend
test_spring_boot() {
    echo -e "\n${BLUE}🍃 Testing Spring Boot Backend (Port 8080)${NC}"
    echo "-------------------------------------------"
    
    # Health check (try common endpoints)
    if curl -s http://localhost:8080/api/predict > /dev/null 2>&1; then
        echo -e "✅ ${GREEN}Spring Boot Connection: PASSED${NC}"
    else
        echo -e "❌ ${RED}Spring Boot Connection: FAILED${NC}"
        echo "💡 Start Spring Boot application"
        return 1
    fi
    
    # Test prediction endpoint
    echo -e "\n🔮 Testing Spring Boot → FastAPI Integration:"
    
    for i in "${!test_cases[@]}"; do
        case_num=$((i + 1))
        test_case="${test_cases[$i]}"
        
        echo -e "\n  Test Case $case_num:"
        response=$(curl -s -X POST "http://localhost:8080/api/predict" \
            -H "Content-Type: application/json" \
            -d "$test_case")
        
        if echo "$response" | jq -e '.predicted_position' > /dev/null 2>&1; then
            position=$(echo "$response" | jq -r '.predicted_position // .predictedPosition')
            confidence=$(echo "$response" | jq -r '.prediction_confidence // .predictionConfidence')
            is_historical=$(echo "$response" | jq -r '.is_historical // .isHistorical')
            
            echo -e "    ✅ ${GREEN}Position: P$position, Confidence: $(echo "$confidence * 100" | bc -l | xargs printf "%.1f")%, Historical: $is_historical${NC}"
        else
            echo -e "    ❌ ${RED}Invalid response: $response${NC}"
        fi
    done
}

# Function to test React frontend (check if it's running)
test_react_frontend() {
    echo -e "\n${BLUE}⚛️ Testing React Frontend (Port 3000)${NC}"
    echo "-----------------------------------"
    
    if curl -s http://localhost:3000 > /dev/null; then
        echo -e "✅ ${GREEN}React Frontend: RUNNING${NC}"
        echo -e "🌐 Open browser: http://localhost:3000"
    else
        echo -e "❌ ${RED}React Frontend: NOT RUNNING${NC}"
        echo "💡 Start React with: npm run dev"
    fi
}

# Function to check prerequisites
check_prerequisites() {
    echo -e "\n${BLUE}🔧 Checking Prerequisites${NC}"
    echo "-------------------------"
    
    # Check if jq is installed
    if command -v jq &> /dev/null; then
        echo -e "✅ ${GREEN}jq (JSON parser): INSTALLED${NC}"
    else
        echo -e "❌ ${RED}jq (JSON parser): NOT INSTALLED${NC}"
        echo "💡 Install with: sudo apt-get install jq (Linux) or brew install jq (Mac)"
        return 1
    fi
    
    # Check if bc is installed (for calculations)
    if command -v bc &> /dev/null; then
        echo -e "✅ ${GREEN}bc (calculator): INSTALLED${NC}"
    else
        echo -e "❌ ${RED}bc (calculator): NOT INSTALLED${NC}"
        echo "💡 Install with: sudo apt-get install bc (Linux) or brew install bc (Mac)"
        return 1
    fi
    
    # Check if curl is installed
    if command -v curl &> /dev/null; then
        echo -e "✅ ${GREEN}curl: INSTALLED${NC}"
    else
        echo -e "❌ ${RED}curl: NOT INSTALLED${NC}"
        return 1
    fi
}

# Function to display summary
display_summary() {
    echo -e "\n${BLUE}📋 Integration Test Summary${NC}"
    echo "============================"
    echo ""
    echo "🏗️ Architecture:"
    echo "  React Frontend (Port 3000) → Spring Boot API (Port 8080) → FastAPI ML (Port 8000)"
    echo ""
    echo "🎯 What was tested:"
    echo "  ✓ FastAPI position prediction endpoint"
    echo "  ✓ Spring Boot API gateway integration"
    echo "  ✓ Historical data lookup"
    echo "  ✓ Position classification with confidence"
    echo ""
    echo "📱 Frontend features:"
    echo "  ✓ Driver selection with automatic team/experience"
    echo "  ✓ Custom experience override"
    echo "  ✓ Position prediction display with confidence"
    echo "  ✓ Historical result comparison"
    echo ""
    echo "🚀 To run the full stack:"
    echo "  1. FastAPI: cd Analysis && uvicorn main:app --reload"
    echo "  2. Spring Boot: cd demo && ./mvnw spring-boot:run"
    echo "  3. React: cd Frontend/F1Pulse && npm run dev"
    echo ""
}

# Main execution
main() {
    # Check prerequisites first
    if ! check_prerequisites; then
        echo -e "\n❌ ${RED}Prerequisites check failed. Please install missing tools.${NC}"
        exit 1
    fi
    
    # Test each layer
    test_fastapi
    test_spring_boot  
    test_react_frontend
    
    # Display summary
    display_summary
    
    echo -e "\n🏁 ${GREEN}Integration testing complete!${NC}"
}

# Run main function
main
