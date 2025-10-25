#!/bin/bash
# Launch NetGuard AI Dashboard

cd /home/dave/Documents/NetGuardAI
source .venv/bin/activate

echo "🛡️  Launching NetGuard AI Dashboard..."
echo ""
echo "Dashboard will be available at:"
echo "  Local:   http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the dashboard"
echo ""

cd dashboard
../.venv/bin/streamlit run app.py
