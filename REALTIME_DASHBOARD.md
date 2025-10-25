# 🎨 Real-Time Dashboard Integration - Complete Guide

## ✅ What's Been Implemented

Your NetGuard AI now has a **professional real-time dashboard** with full ML integration!

### New Components:

1. **`dashboard/app_realtime.py`** - Advanced real-time dashboard
   - Live metrics updating every 1-2 seconds
   - Real-time threat alerts with animations
   - Interactive charts with Plotly
   - ML prediction visualization
   - Export functionality
   - Auto-refresh capability

2. **`launch_realtime.sh`** - Easy launcher script
   - Integrated mode (analyzer + dashboard)
   - Dashboard-only mode
   - Analyzer-only mode

3. **`launch_integrated.py`** - Python integrated launcher
   - Starts both services together
   - Process management
   - Graceful shutdown

4. **Dashboard Data Integration** in `realtime_analyzer.py`
   - Writes predictions to `data/ml_predictions.json`
   - Updates stats in `data/ml_stats.json`
   - Thread-safe file operations

---

## 🚀 Quick Start

### Option 1: Simple Launch (Recommended)
```bash
./launch_realtime.sh
```
Then select:
- **Option 1**: Run both analyzer & dashboard
- **Option 2**: Dashboard only (view existing data)
- **Option 3**: Analyzer only

### Option 2: Manual Launch

**Terminal 1 - Start Analyzer:**
```bash
sudo .venv/bin/python realtime_analyzer.py --model models/threat_detector.joblib
```

**Terminal 2 - Start Dashboard:**
```bash
cd dashboard
../.venv/bin/streamlit run app_realtime.py
```

### Option 3: Integrated Python Launcher
```bash
sudo .venv/bin/python launch_integrated.py
```

---

## 📊 Dashboard Features

### 1. **Live Metrics** (Updates every 1-2 seconds)
- 📦 Total Packets Captured
- 🔍 Windows Processed
- 📊 Mean/Max/Min Packet Size
- ✅ Normal vs 🚨 Threat Count

### 2. **Real-Time Threat Alerts**
- 🚨 Flashing red banner for active threats
- Threat type and confidence display
- Time since detection
- Toast notifications

### 3. **Interactive Visualizations**
- **Traffic Analysis Tab:**
  - Protocol distribution pie chart
  - Top source IPs bar chart
  - Packet size distribution histogram

- **ML Predictions Tab:**
  - Normal vs Threat classification
  - Threat types breakdown
  - Confidence score distribution

- **Threat Details Tab:**
  - Live threat log table
  - Latest threat feature values
  - Detailed metrics

- **Time Series Tab:**
  - Packets per minute line chart
  - Bytes transferred area chart
  - Predictions over time

### 4. **Auto-Refresh**
- Toggle on/off
- Configurable refresh rate (1-10 seconds)
- Default: 2 seconds

### 5. **Time Filtering**
- Last 5 minutes
- Last 15 minutes
- Last hour
- Last 24 hours
- All time

### 6. **Export Functionality**
- Export all logs to CSV
- Timestamped filenames
- One-click download

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────┐
│         Backend (realtime_analyzer.py)      │
│                                             │
│  ┌──────────┐         ┌─────────────────┐ │
│  │ Packet   │         │ Feature         │ │
│  │ Capture  │────────▶│ Extraction      │ │
│  │ (Thread) │         │ (27 features)   │ │
│  └──────────┘         └─────────────────┘ │
│                              │             │
│                              ▼             │
│                     ┌─────────────────┐   │
│                     │ ML Prediction   │   │
│                     │ (Random Forest) │   │
│                     └─────────────────┘   │
│                              │             │
│                              ▼             │
│     ┌────────────────────────────────────┐│
│     │  File-Based Data Exchange          ││
│     │  (Thread-Safe JSON Files)          ││
│     │                                    ││
│     │  • ml_predictions.json (1000 max) ││
│     │  • ml_stats.json (live stats)     ││
│     └────────────────────────────────────┘│
└─────────────────┬───────────────────────────┘
                  │
                  │ Read every 1-2 seconds
                  │
                  ▼
┌─────────────────────────────────────────────┐
│      Frontend (app_realtime.py)             │
│                                             │
│  ┌────────────────────────────────────────┐│
│  │  Streamlit Dashboard                   ││
│  │                                        ││
│  │  • Auto-refresh (1-2s)                ││
│  │  • Live metrics                       ││
│  │  • Threat alerts                      ││
│  │  • Interactive charts                 ││
│  │  • Time filtering                     ││
│  │  • Export functionality               ││
│  └────────────────────────────────────────┘│
│                                             │
│          User Browser (localhost:8501)      │
└─────────────────────────────────────────────┘
```

---

## 🔧 How It Works

### Data Flow:

1. **Backend (Analyzer)**:
   - Captures packets continuously
   - Extracts 27 features every 5 seconds
   - Runs ML prediction
   - **Writes to JSON files** (thread-safe)

2. **File-Based Communication**:
   - `data/ml_predictions.json` - Last 1000 predictions
   - `data/ml_stats.json` - Current statistics
   - Files updated after each prediction window

3. **Frontend (Dashboard)**:
   - Reads JSON files every 1-2 seconds
   - Parses and displays data
   - Auto-refreshes using `st.rerun()`
   - Maintains session state for alerts

### Thread Safety:
- Each write is atomic (full file rewrite)
- Dashboard reads are non-blocking
- No race conditions
- Graceful handling of missing/corrupted files

---

## 📝 Configuration

### Dashboard Settings (Sidebar):

**Auto-Refresh:**
```python
auto_refresh = True  # Enable/disable
refresh_rate = 2     # Seconds (1-10)
```

**Time Filter:**
- Filters data by time range
- Applies to all visualizations

**Export:**
- Creates timestamped CSV files
- Exports packets, threats, and ML predictions

---

## 🎯 Real-Time Features

### 1. **Live Updates** (1-2 second delay)
- Metrics update automatically
- Charts refresh with new data
- Threat log appends new entries
- No manual refresh needed

### 2. **Threat Alerts**
- Animated red banner for threats <30s old
- Shows threat type, confidence, time
- Browser toast notifications
- Visual feedback

### 3. **Performance**
- Lightweight JSON file reads
- Efficient Pandas operations
- Plotly hardware acceleration
- Minimal CPU usage

---

## 🚀 Launch Methods Comparison

### Method 1: launch_realtime.sh (Easiest)
```bash
./launch_realtime.sh
# Select option 1 for integrated mode
```
✅ Simple menu interface  
✅ Auto-detects ML model  
✅ Handles process management  
⚠️ Basic cleanup on exit

### Method 2: Manual (Most Control)
```bash
# Terminal 1
sudo .venv/bin/python realtime_analyzer.py --model models/threat_detector.joblib

# Terminal 2
cd dashboard && ../.venv/bin/streamlit run app_realtime.py
```
✅ Full control  
✅ See all logs  
✅ Easy debugging  
⚠️ Manual process management

### Method 3: launch_integrated.py (Most Robust)
```bash
sudo .venv/bin/python launch_integrated.py
```
✅ Single command  
✅ Process monitoring  
✅ Graceful shutdown  
✅ Error handling

---

## 📊 Data Files

### ml_predictions.json
```json
[
  {
    "timestamp": "2025-10-24T19:30:15.123456",
    "is_threat": false,
    "threat_type": "normal",
    "confidence": 0.95,
    "features": {
      "total_packets": 45,
      "total_bytes": 23450,
      ...
    }
  }
]
```
- Stores last 1000 predictions
- Updated after each window (5s)
- Used by dashboard for visualization

### ml_stats.json
```json
{
  "running": true,
  "window_size": 5,
  "total_packets": 15234,
  "total_predictions": 304,
  "threats_detected": 12,
  "buffer_size": 145,
  "prediction_queue_size": 3,
  "last_update": "2025-10-24T19:30:15.123456"
}
```
- Current analyzer statistics
- Updated after each prediction
- Shows system status

---

## 🎨 Dashboard Customization

### Change Refresh Rate:
Edit `app_realtime.py`:
```python
refresh_rate = st.slider("Refresh rate (seconds)", 1, 10, 2)
```

### Add Custom Charts:
```python
# In the appropriate tab
fig = px.scatter(df, x='feature1', y='feature2', color='is_threat')
st.plotly_chart(fig, use_container_width=True)
```

### Customize Alerts:
```python
# Adjust alert threshold
if time_since < 30:  # Change to 60 for 1-minute alerts
    st.markdown(f"""<div class="threat-alert">...</div>""")
```

---

## 🔍 Troubleshooting

### Dashboard shows "No data"
1. Check if analyzer is running
2. Verify JSON files exist in `data/`
3. Check file permissions
4. Look for errors in analyzer logs

### Slow Performance
1. Reduce refresh rate (increase to 5-10s)
2. Limit time filter range
3. Check system resources
4. Reduce prediction buffer size

### Analyzer stops unexpectedly
1. Check sudo permissions
2. Verify network interface
3. Check available memory
4. Review analyzer logs

### Port 8501 already in use
```bash
# Find and kill existing process
lsof -ti:8501 | xargs kill -9

# Or use different port
streamlit run app_realtime.py --server.port 8502
```

---

## ✅ Verification

### Test Dashboard (Without Analyzer):
```bash
cd dashboard
../.venv/bin/streamlit run app_realtime.py
```
Should show existing data from `data/` folder.

### Test Integration:
```bash
# Generate test predictions
.venv/bin/python test_ml_integration.py

# Launch dashboard
cd dashboard && ../.venv/bin/streamlit run app_realtime.py
```

### Monitor Data Files:
```bash
# Watch predictions file
watch -n 1 'tail -20 data/ml_predictions.json'

# Watch stats file
watch -n 1 'cat data/ml_stats.json'
```

---

## 🎉 Success Criteria - ALL MET

- [x] Real-time updates (1-2s delay) ✅
- [x] Live packet metrics ✅
- [x] Mean/Max/Min packet size ✅
- [x] Normal vs threat counts ✅
- [x] Visual threat alerts ✅
- [x] Interactive Plotly charts ✅
- [x] Threat log table ✅
- [x] CSV export ✅
- [x] Auto-refresh ✅
- [x] Backend integration (file-based) ✅
- [x] Thread safety ✅
- [x] Graceful termination ✅
- [x] Professional UI ✅
- [x] Nothing broken ✅

---

## 🚀 You Now Have:

1. ✅ **Real-time dashboard** with 1-2 second updates
2. ✅ **Live threat alerts** with animations
3. ✅ **Interactive visualizations** with Plotly
4. ✅ **ML prediction display** with confidence scores
5. ✅ **Thread-safe integration** via JSON files
6. ✅ **Auto-refresh** capability
7. ✅ **Export functionality** to CSV
8. ✅ **Multiple launch methods**
9. ✅ **Professional UI** with custom styling
10. ✅ **Zero breaking changes** to existing system

**Your original dashboard still works perfectly!**  
New dashboard is at: `dashboard/app_realtime.py`  
Original is at: `dashboard/app.py`

---

## 🎯 Quick Commands

```bash
# Launch integrated system
./launch_realtime.sh

# Dashboard only
cd dashboard && ../.venv/bin/streamlit run app_realtime.py

# Original dashboard (still works!)
cd dashboard && ../.venv/bin/streamlit run app.py

# Train model first
.venv/bin/python train_model.py

# Test integration
.venv/bin/python test_ml_integration.py
```

---

## 📚 Next Steps

1. **Train the model**: `.venv/bin/python train_model.py`
2. **Launch system**: `./launch_realtime.sh`
3. **Open browser**: http://localhost:8501
4. **Watch threats** appear in real-time!

🎉 **Enjoy your enterprise-grade real-time threat monitoring dashboard!** 🎉
