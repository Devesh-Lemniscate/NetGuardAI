#!/bin/bash

# NetGuard AI - Complete Dashboard Launcher

echo "🛡️  NetGuard AI - Complete Dashboard"
echo "===================================="
echo ""

cd "$(dirname "$0")/dashboard"

echo "🚀 Starting complete dashboard on http://localhost:8501"
echo ""
echo "📋 What you can do from the dashboard:"
echo "   ✅ Train ML model"
echo "   ✅ Start/Stop real-time analyzer"
echo "   ✅ Generate sample data"
echo "   ✅ Monitor live traffic"
echo "   ✅ View ML predictions"
echo "   ✅ Analyze threats"
echo "   ✅ Export data as CSV"
echo "   ✅ Auto-refresh controls"
echo ""
echo "Press Ctrl+C to stop"
echo ""

../.venv/bin/streamlit run app_complete.py --server.port 8501
