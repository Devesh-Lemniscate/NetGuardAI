#!/bin/bash
# NetGuard AI - Project Launcher

echo "🛡️  NetGuard AI - Network Threat Detection System"
echo "=================================================="
echo ""

# Color codes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "${YELLOW}Virtual environment not found. Creating one...${NC}"
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
else
    source .venv/bin/activate
fi

echo ""
echo "${GREEN}✓ Virtual environment activated${NC}"
echo ""
echo "Select an option:"
echo "1) Start Packet Capture (requires sudo)"
echo "2) Launch Dashboard (Streamlit)"
echo "3) Generate Sample Data"
echo "4) View Captured Packets"
echo "5) View Threat Logs"
echo "6) Check System Status"
echo "7) Train ML Model"
echo "8) Run Real-Time ML Analyzer (requires sudo)"
echo "9) Launch Real-Time Dashboard"
echo "10) Launch COMPLETE Dashboard (ALL FEATURES IN GUI) ⭐ NEW!"
echo "0) Exit"
echo ""
read -p "Enter choice [0-10]: " choice

case $choice in
    1)
        echo ""
        echo "${BLUE}Starting packet capture...${NC}"
        echo "${YELLOW}Note: Packet capture requires sudo/root privileges${NC}"
        sudo .venv/bin/python main.py
        ;;
    2)
        echo ""
        echo "${BLUE}Launching Streamlit Dashboard...${NC}"
        cd dashboard && ../.venv/bin/streamlit run app.py
        ;;
    3)
        echo ""
        echo "${BLUE}Generating sample data...${NC}"
        .venv/bin/python generate_sample_data.py
        echo ""
        echo "${GREEN}Done! You can now launch the dashboard to view the data.${NC}"
        ;;
    4)
        echo ""
        if [ -f "data/packets_log.csv" ]; then
            echo "${GREEN}Recent packets:${NC}"
            head -20 data/packets_log.csv
        else
            echo "${YELLOW}No packet data found. Run packet capture first.${NC}"
        fi
        ;;
    5)
        echo ""
        if [ -f "data/threat_logs.json" ]; then
            echo "${GREEN}Recent threats:${NC}"
            cat data/threat_logs.json | .venv/bin/python -m json.tool | head -50
        else
            echo "${YELLOW}No threat logs found. Run packet capture first.${NC}"
        fi
        ;;
    6)
        echo ""
        echo "${BLUE}System Status:${NC}"
        echo "Python: $(.venv/bin/python --version)"
        echo "Virtual Env: $(pwd)/.venv"
        echo ""
        .venv/bin/python -c "import scapy, pandas, streamlit; print('✅ All core packages installed')"
        echo ""
        if [ -f "data/packets_log.csv" ]; then
            PACKET_COUNT=$(wc -l < data/packets_log.csv)
            echo "📦 Packets logged: $PACKET_COUNT"
        else
            echo "📦 Packets logged: 0"
        fi
        if [ -f "data/threat_logs.json" ]; then
            echo "🚨 Threat log exists"
        else
            echo "🚨 No threat logs yet"
        fi
        ;;
    7)
        echo ""
        echo "${BLUE}Training ML model...${NC}"
        .venv/bin/python train_model.py
        echo ""
        echo "${GREEN}Model training complete!${NC}"
        echo "Model saved to: models/threat_detector.joblib"
        ;;
    8)
        echo ""
        echo "${BLUE}Starting Real-Time ML Analyzer...${NC}"
        echo "${YELLOW}Note: Requires sudo/root privileges${NC}"
        echo ""
        if [ -f "models/threat_detector.joblib" ]; then
            echo "Using ML model: models/threat_detector.joblib"
            sudo .venv/bin/python realtime_analyzer.py --model models/threat_detector.joblib
        else
            echo "${YELLOW}No ML model found. Using rule-based detection.${NC}"
            echo "Tip: Run option 7 to train a model first."
            echo ""
            sudo .venv/bin/python realtime_analyzer.py
        fi
        ;;
    9)
        echo ""
        echo "${BLUE}Launching Real-Time Dashboard...${NC}"
        echo "This is the new ML-integrated dashboard with live updates!"
        echo ""
        cd dashboard && ../.venv/bin/streamlit run app_realtime.py
        ;;
    10)
        echo ""
        echo "${GREEN}🛡️  Launching COMPLETE Dashboard - ALL FEATURES IN GUI! ⭐${NC}"
        echo ""
        echo "✨ What you can do from this dashboard:"
        echo "   ✅ Train ML model (click button)"
        echo "   ✅ Start/Stop analyzer (click button)"
        echo "   ✅ Generate test data (click button)"
        echo "   ✅ Monitor live traffic"
        echo "   ✅ View ML predictions"
        echo "   ✅ Analyze threats"
        echo "   ✅ Export data as CSV"
        echo "   ✅ Auto-refresh controls"
        echo ""
        echo "📖 See COMPLETE_FEATURES_GUIDE.md for full documentation"
        echo ""
        echo "Opening at: http://localhost:8501"
        echo ""
        cd dashboard && ../.venv/bin/streamlit run app_complete.py
        ;;
    0)
        echo ""
        echo "${GREEN}Goodbye!${NC}"
        exit 0
        ;;
    *)
        echo "${YELLOW}Invalid choice${NC}"
        ;;
esac
