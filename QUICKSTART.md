# 🚀 NetGuard AI - Quick Start Guide

## ✅ Setup Complete!

Your NetGuard AI project is now fully configured with:
- ✓ Python virtual environment (`.venv`)
- ✓ All dependencies installed
- ✓ Dashboard application created
- ✓ Data directories initialized

---

## 📋 Project Components

### 1. **Packet Capture** (`main.py`)
Captures live network traffic and logs it to CSV files.

### 2. **Threat Detection** (`threat_model.py`)
Analyzes captured packets for suspicious activity.

### 3. **Dashboard** (`dashboard/app.py`)
Web-based visualization using Streamlit.

### 4. **Feature Extraction** (`feature_extractor.py`)
Extracts features from packets for ML analysis.

---

## 🎯 How to Run

### Option 1: Using the Launch Script (Recommended)
```bash
./run.sh
```
Then select from the menu:
1. Start Packet Capture
2. Launch Dashboard
3. Run Tests
4. View Captured Packets
5. View Threat Logs

### Option 2: Manual Commands

#### Start Packet Capture (requires sudo)
```bash
source .venv/bin/activate
sudo .venv/bin/python main.py
# Or specify interface:
sudo .venv/bin/python main.py --interface eth0
```

#### Launch Dashboard
```bash
source .venv/bin/activate
cd dashboard
streamlit run app.py
```
The dashboard will open at: http://localhost:8501

---

## ⚠️ Important Notes

### Permissions Required
- **Packet capture requires root/sudo privileges** to access network interfaces
- Run with: `sudo .venv/bin/python main.py`

### Network Interfaces
To see available network interfaces:
```bash
ip link show
# or
ifconfig
```

Common interfaces:
- `eth0` - Ethernet
- `wlan0` - WiFi
- `lo` - Loopback
- `enp0s3` - VirtualBox/VM network

---

## 📊 Data Files

All data is stored in the `data/` directory:
- **packets_log.csv** - Captured network packets
- **threat_logs.json** - Detected threats and anomalies

---

## 🔧 Troubleshooting

### "Operation not permitted" Error
Solution: Run with sudo
```bash
sudo .venv/bin/python main.py
```

### No packets captured
- Check if you specified the correct interface
- Ensure you have network traffic
- Try without interface specification (uses default)

### Dashboard shows no data
- First run packet capture to generate data
- Check that `data/packets_log.csv` exists
- Refresh the dashboard

---

## 🧪 Testing the Setup

### Quick Test (without sudo)
```bash
source .venv/bin/activate
python -c "import scapy, pandas, streamlit; print('✓ All packages working!')"
```

### Test Dashboard
```bash
cd dashboard
streamlit run app.py
```

### Generate Sample Data
If you want to test without capturing live packets, you can manually create sample data:
```bash
source .venv/bin/activate
python -c "
import pandas as pd
from datetime import datetime
import os
os.makedirs('data', exist_ok=True)
data = {
    'Timestamp': [datetime.now()] * 10,
    'Src_IP': ['192.168.1.100'] * 10,
    'Dst_IP': ['8.8.8.8'] * 10,
    'Protocol': [6] * 10,
    'Src_Port': [50000 + i for i in range(10)],
    'Dst_Port': [443] * 10,
    'Size': [1500] * 10
}
pd.DataFrame(data).to_csv('data/packets_log.csv', index=False)
print('✓ Sample data created!')
"
```

---

## 📚 Next Steps

1. **Start capturing packets** to collect network data
2. **Monitor the dashboard** for real-time visualization
3. **Check threat logs** for detected anomalies
4. **Explore Jupyter notebooks** in `jupyter_notebooks/` for analysis
5. **Train ML models** for advanced threat detection

---

## 🛠️ Virtual Environment Commands

Activate virtual environment:
```bash
source .venv/bin/activate
```

Deactivate when done:
```bash
deactivate
```

Install additional packages:
```bash
source .venv/bin/activate
pip install <package-name>
```

---

## 📖 Additional Resources

- **Scapy Documentation**: https://scapy.readthedocs.io/
- **Streamlit Documentation**: https://docs.streamlit.io/
- **Pandas Documentation**: https://pandas.pydata.org/docs/

---

## 🎉 You're Ready!

Your NetGuard AI system is fully set up and ready to monitor network traffic!

For questions or issues, check the main README.md file.
