#!/bin/bash
# NetGuard AI - Simple Test Script

echo "🧪 Testing NetGuard AI Components..."
echo "====================================="

cd /home/dave/Documents/NetGuardAI

# Test 1: Virtual environment
echo "1. Testing virtual environment..."
if [ -d ".venv" ]; then
    echo "   ✅ Virtual environment exists"
    source .venv/bin/activate
    echo "   ✅ Virtual environment activated"
else
    echo "   ❌ Virtual environment missing"
    exit 1
fi

# Test 2: Python imports
echo "2. Testing Python imports..."
.venv/bin/python -c "
import sys
try:
    import scapy.all
    print('   ✅ scapy imported')
    import pandas
    print('   ✅ pandas imported')
    import streamlit
    print('   ✅ streamlit imported')
    import plotly
    print('   ✅ plotly imported')
    print('   ✅ All packages working!')
except ImportError as e:
    print(f'   ❌ Import error: {e}')
    sys.exit(1)
"

# Test 3: Project modules
echo "3. Testing project modules..."
.venv/bin/python -c "
try:
    from threat_model import ThreatDetector
    print('   ✅ ThreatDetector imported')
    from feature_extractor import extract_features
    print('   ✅ extract_features imported')
    print('   ✅ All project modules working!')
except ImportError as e:
    print(f'   ❌ Module error: {e}')
"

# Test 4: Data directory
echo "4. Testing data directory..."
if [ -d "data" ]; then
    echo "   ✅ Data directory exists"
    ls -la data/
else
    echo "   ❌ Data directory missing"
    mkdir -p data
    echo "   ✅ Data directory created"
fi

# Test 5: Dashboard
echo "5. Testing dashboard..."
if [ -f "dashboard/app.py" ]; then
    echo "   ✅ Dashboard app exists"
else
    echo "   ❌ Dashboard app missing"
fi

echo ""
echo "🎉 All tests completed!"
echo ""
echo "📋 How to run:"
echo "   Packet Capture: sudo .venv/bin/python main.py"
echo "   Dashboard:      cd dashboard && ../.venv/bin/streamlit run app.py"
echo "   Or use:         ./run.sh"
echo ""
