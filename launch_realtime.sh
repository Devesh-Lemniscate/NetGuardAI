#!/bin/bash
# Simple launcher for NetGuard AI with Real-Time Dashboard

echo "╔══════════════════════════════════════════════════════════╗"
echo "║     🛡️  NetGuard AI - Real-Time System Launcher          ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

cd /home/dave/Documents/NetGuardAI

# Check if model exists
if [ ! -f "models/threat_detector.joblib" ]; then
    echo "⚠️  ML model not found!"
    echo "   Train it first: .venv/bin/python train_model.py"
    echo ""
    read -p "Continue without ML model? (y/n): " response
    if [ "$response" != "y" ]; then
        exit 1
    fi
    MODEL_ARG=""
else
    MODEL_ARG="--model models/threat_detector.joblib"
    echo "✅ ML model found"
fi

echo ""
echo "📋 Choose launch mode:"
echo "1) Analyzer + Dashboard (integrated, requires sudo)"
echo "2) Dashboard only (view existing data)"
echo "3) Analyzer only (requires sudo)"
echo ""
read -p "Enter choice [1-3]: " choice

case $choice in
    1)
        echo ""
        echo "🚀 Launching integrated system..."
        echo ""
        echo "This will start:"
        echo "  1. ML Analyzer (background)"
        echo "  2. Real-Time Dashboard"
        echo ""
        echo "Dashboard will be at: http://localhost:8501"
        echo "Press Ctrl+C to stop both"
        echo ""
        
        # Start analyzer in background
        sudo .venv/bin/python realtime_analyzer.py $MODEL_ARG &
        ANALYZER_PID=$!
        
        # Wait for analyzer to start
        sleep 3
        
        # Start dashboard
        cd dashboard
        ../.venv/bin/streamlit run app_realtime.py
        
        # Cleanup when dashboard stops
        sudo kill $ANALYZER_PID 2>/dev/null
        ;;
    
    2)
        echo ""
        echo "🎨 Launching Dashboard only..."
        cd dashboard
        ../.venv/bin/streamlit run app_realtime.py
        ;;
    
    3)
        echo ""
        echo "📡 Launching Analyzer only..."
        sudo .venv/bin/python realtime_analyzer.py $MODEL_ARG
        ;;
    
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac
