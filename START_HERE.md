# 🎯 NetGuard AI - READY TO RUN!

## ✅ Setup Complete!

Everything is installed and configured. Your project is ready to use!

---

## 🚀 Quick Start (Choose One Method)

### Method 1: Interactive Menu (Easiest)
```bash
./run.sh
```
Then select an option from the menu.

### Method 2: Direct Commands

#### Launch Dashboard
```bash
./launch_dashboard.sh
```
Or manually:
```bash
cd dashboard && ../.venv/bin/streamlit run app.py
```
Dashboard will be at: **http://localhost:8501**

#### Generate Sample Data (for testing)
```bash
.venv/bin/python generate_sample_data.py
```

#### Start Packet Capture (requires sudo)
```bash
sudo .venv/bin/python main.py
```

---

## 📊 What You Can Do Now

### 1️⃣ View the Dashboard (Recommended First Step)
Sample data has already been generated! Launch the dashboard to see it:
```bash
./launch_dashboard.sh
```

### 2️⃣ Capture Real Network Traffic
```bash
sudo .venv/bin/python main.py
```
**Note:** Requires root/sudo privileges to access network interface

### 3️⃣ Generate More Sample Data
```bash
.venv/bin/python generate_sample_data.py
```

---

## 🗂️ Project Structure

```
NetGuardAI/
├── .venv/                    # Virtual environment (✅ configured)
├── dashboard/
│   └── app.py               # Streamlit dashboard (✅ working)
├── data/
│   ├── packets_log.csv      # Network packets (✅ sample data ready)
│   └── threat_logs.json     # Detected threats (✅ sample data ready)
├── main.py                  # Packet capture script
├── threat_model.py          # Threat detection logic
├── feature_extractor.py     # Feature extraction
├── generate_sample_data.py  # Sample data generator (✅ ready)
├── launch_dashboard.sh      # Dashboard launcher (✅ ready)
├── run.sh                   # Interactive menu (✅ ready)
└── requirements.txt         # Dependencies (✅ installed)
```

---

## 🛠️ Common Commands

### Activate Virtual Environment
```bash
source .venv/bin/activate
```

### Check System Status
```bash
./run.sh   # Then select option 6
```

### View Packet Logs
```bash
head -20 data/packets_log.csv
```

### View Threat Logs
```bash
cat data/threat_logs.json | .venv/bin/python -m json.tool
```

---

## ⚡ Troubleshooting

### Dashboard won't start?
- Make sure port 8501 is not in use
- Check: `lsof -i :8501`
- Kill process if needed: `kill -9 <PID>`

### Permission denied for packet capture?
- Use sudo: `sudo .venv/bin/python main.py`

### No data showing in dashboard?
- Generate sample data first: `.venv/bin/python generate_sample_data.py`
- Or run packet capture to collect real data

---

## 🎉 You're All Set!

**Start with this:**
```bash
./launch_dashboard.sh
```

Then open your browser to: **http://localhost:8501**

You'll see:
- 📦 100 sample packets captured
- 🚨 20 sample threats detected
- 📊 Interactive charts and visualizations

---

## 📝 Next Steps

1. ✅ View the dashboard with sample data
2. ✅ Capture real network traffic
3. ✅ Explore the Jupyter notebooks in `jupyter_notebooks/`
4. ✅ Train ML models for better threat detection
5. ✅ Customize the threat detection rules

**Happy monitoring! 🛡️**
