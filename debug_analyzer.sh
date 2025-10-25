#!/bin/bash

echo "🔍 TROUBLESHOOTING REAL-TIME ANALYZER"
echo "======================================"
echo ""

echo "1️⃣ Checking if analyzer processes are running..."
ANALYZER_PROCS=$(ps aux | grep realtime_analyzer | grep -v grep | wc -l)
echo "   Found $ANALYZER_PROCS analyzer processes"
echo ""

echo "2️⃣ Killing all stuck analyzer processes..."
sudo pkill -9 -f realtime_analyzer
sleep 2
echo "   Done!"
echo ""

echo "3️⃣ Checking for prediction files..."
if [ -f "data/ml_predictions.json" ]; then
    echo "   ✅ ml_predictions.json exists"
    echo "   Last modified: $(stat -c %y data/ml_predictions.json)"
    echo "   Size: $(stat -c %s data/ml_predictions.json) bytes"
else
    echo "   ❌ ml_predictions.json does NOT exist"
fi

if [ -f "data/ml_stats.json" ]; then
    echo "   ✅ ml_stats.json exists"
    echo "   Last modified: $(stat -c %y data/ml_stats.json)"
else
    echo "   ❌ ml_stats.json does NOT exist"
fi
echo ""

echo "4️⃣ Checking network interfaces..."
echo "   Available interfaces:"
ip -br link | grep -v "^lo" | head -5
echo ""

echo "5️⃣ Testing if analyzer can start (will run for 10 seconds)..."
echo "   Starting analyzer..."
timeout 10 sudo .venv/bin/python realtime_analyzer.py --model models/threat_detector.joblib 2>&1 &
ANALYZER_PID=$!
sleep 2

echo ""
echo "6️⃣ Generating test traffic..."
ping -c 5 8.8.8.8 > /dev/null 2>&1 &
curl -s https://google.com > /dev/null 2>&1 &
curl -s https://github.com > /dev/null 2>&1 &
echo "   Generated test traffic (ping + web requests)"
sleep 5

echo ""
echo "7️⃣ Checking if prediction files were created..."
if [ -f "data/ml_predictions.json" ]; then
    echo "   ✅ ml_predictions.json was created!"
    echo "   Content preview:"
    head -5 data/ml_predictions.json
else
    echo "   ❌ ml_predictions.json was NOT created"
    echo "   This means the analyzer is not capturing packets!"
fi

if [ -f "data/ml_stats.json" ]; then
    echo "   ✅ ml_stats.json was created!"
else
    echo "   ❌ ml_stats.json was NOT created"
fi

echo ""
echo "8️⃣ Stopping test analyzer..."
sudo pkill -f realtime_analyzer
sleep 1

echo ""
echo "======================================"
echo "🎯 DIAGNOSIS:"
echo ""
if [ -f "data/ml_predictions.json" ]; then
    echo "✅ Analyzer CAN capture packets!"
    echo "   The problem is likely the dashboard not reading the files."
    echo ""
    echo "💡 SOLUTION:"
    echo "   1. Make sure auto-refresh is ON in the dashboard"
    echo "   2. Wait 5-10 seconds after starting analyzer"
    echo "   3. Check the 'Live Monitoring' tab"
else
    echo "❌ Analyzer CANNOT capture packets!"
    echo ""
    echo "💡 POSSIBLE ISSUES:"
    echo "   1. Permission problem (need sudo)"
    echo "   2. Wrong network interface"
    echo "   3. Python/scapy not working"
    echo ""
    echo "💡 SOLUTIONS TO TRY:"
    echo "   1. Run: sudo .venv/bin/python realtime_analyzer.py"
    echo "   2. Check for errors in terminal"
    echo "   3. Try different network interface with --interface flag"
fi

echo ""
echo "======================================"
