#!/bin/bash

echo "🚀 STARTING NETGUARD AI - COMPLETE SYSTEM"
echo "=========================================="
echo ""

# Get the script directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

echo "📁 Working directory: $DIR"
echo ""

# Kill any existing processes
echo "🧹 Cleaning up old processes..."
sudo pkill -f realtime_analyzer 2>/dev/null
pkill -f streamlit 2>/dev/null
sleep 2

# Detect active network interface
echo "🔍 Detecting network interface..."
INTERFACE=$(ip -br link | grep -v "^lo" | grep "UP" | head -1 | awk '{print $1}')

if [ -z "$INTERFACE" ]; then
    echo "❌ No active network interface found!"
    echo "   Available interfaces:"
    ip -br link
    INTERFACE="any"
fi

echo "✅ Using interface: $INTERFACE"
echo ""

# Create data directory
mkdir -p data

# Start the analyzer in background
echo "📡 Starting Real-Time Analyzer..."
nohup sudo .venv/bin/python realtime_analyzer.py \
    --model models/threat_detector.joblib \
    --interface "$INTERFACE" \
    > data/analyzer.log 2>&1 &

ANALYZER_PID=$!
echo "✅ Analyzer started (PID: $ANALYZER_PID)"
echo "   Logs: data/analyzer.log"
sleep 3

# Check if analyzer is actually running
if ps -p $ANALYZER_PID > /dev/null 2>&1; then
    echo "✅ Analyzer is running!"
else
    echo "⚠️  Analyzer may not be running properly"
    echo "   Check data/analyzer.log for errors"
fi

echo ""

# Start the dashboard
echo "🎨 Starting Dashboard..."
echo "   URL: http://localhost:8501"
echo ""
echo "📊 Dashboard will open in your browser..."
echo "   (If not, manually open: http://localhost:8501)"
echo ""

cd dashboard
../.venv/bin/streamlit run app_complete.py --server.port 8501

# Cleanup on exit
echo ""
echo "🛑 Shutting down..."
sudo pkill -f realtime_analyzer
echo "✅ Done!"
