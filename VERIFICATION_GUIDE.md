# 🔍 VERIFICATION GUIDE - How to Check If Everything Works

## ✅ Quick Status Check

### Step 1: Is the Dashboard Running?
Open your browser to: **http://localhost:8501**
- ✅ If you see the NetGuard AI interface → Dashboard is working!
- ❌ If not → Run `./launch_complete.sh`

---

## 🎯 HOW TO START & VERIFY REAL-TIME ANALYZER

### **Method 1: Start from Dashboard (RECOMMENDED)**

1. **Open Dashboard:** http://localhost:8501

2. **Check Sidebar (Left Side):**
   - Look for "🚀 Real-Time Analyzer Control"
   
3. **Train Model First (if not done):**
   - Click "🎓 Train ML Model" button
   - Wait 30 seconds
   - You'll see "✅ Model trained successfully!"

4. **Start the Analyzer:**
   - Click "▶️ Start Real-Time Analyzer" button
   - **IMPORTANT:** Enter your sudo password when prompted
   - You'll see: "✅ Real-Time Analyzer started successfully!"

5. **Enable Auto-Refresh:**
   - Toggle "🔄 Auto-Refresh Dashboard" to ON
   - Set refresh interval (e.g., 3 seconds)

6. **Watch for Activity:**
   - Go to "📡 Live Monitoring" tab
   - You should see live packet captures appearing
   - Charts will update automatically

---

## 🔬 VERIFICATION CHECKLIST

### ✅ Dashboard Running?
```bash
# Run this command:
ps aux | grep streamlit | grep -v grep
```
**Expected:** You should see a line with `streamlit run app_complete.py`

### ✅ Analyzer Running?
```bash
# Run this command:
ps aux | grep realtime_analyzer | grep -v grep
```
**Expected:** You should see a line with `python realtime_analyzer.py`

### ✅ Files Being Updated?
```bash
# Run this command:
ls -lth data/*.json | head -5
```
**Expected:** `ml_predictions.json` and `ml_stats.json` should show recent timestamps (last few seconds)

### ✅ Network Packets Being Captured?
```bash
# Run this command:
watch -n 2 'wc -l data/packets_log.csv'
```
**Expected:** Line count should be increasing every few seconds

---

## 👀 WHAT YOU SHOULD SEE

### In the Dashboard:

#### **Tab 1: Overview**
- Total packets count (increasing)
- ML predictions count
- Threat detection statistics
- Real-time charts

#### **Tab 2: Live Monitoring** 📡
- Live packet feed (refreshing every 3 seconds)
- Source/Destination IPs
- Protocol types
- Packet sizes
- Status indicators

#### **Tab 3: ML Predictions** 🤖
- Recent ML predictions (last 50)
- Threat/Normal classification
- Confidence scores (%)
- Feature values

#### **Tab 4: Threat Analysis** ⚠️
- Detected threats list
- Threat types
- Severity levels
- Timeline charts

#### **Tab 5: Statistics** 📊
- Protocol distribution (pie charts)
- Top talkers (bar charts)
- Packet size analysis
- Traffic patterns

#### **Tab 6: Features & Guide** 📖
- Feature explanations
- System usage guide
- Quick help

---

## 🚨 TROUBLESHOOTING

### Problem: "Analyzer not starting"
**Solution 1:** Check if you have sudo permissions
```bash
sudo -v
```

**Solution 2:** Check if port 8501 is available
```bash
sudo netstat -tulpn | grep 8501
```

**Solution 3:** Use the command line method:
```bash
# Train model first
.venv/bin/python train_model.py

# Then run analyzer (requires sudo password)
sudo .venv/bin/python realtime_analyzer.py --model models/threat_detector.joblib
```

---

### Problem: "No packets showing up"
**Possible Causes:**
1. **Network interface issue** - Wrong interface selected
2. **No network traffic** - Generate some traffic
3. **Permissions issue** - Analyzer needs sudo

**Solutions:**

**A) Check available network interfaces:**
```bash
ip link show
```

**B) Generate test traffic:**
```bash
# Open another terminal and run:
ping -c 100 8.8.8.8
curl -s https://google.com
```

**C) Check if analyzer is capturing:**
```bash
# Look for error messages
sudo .venv/bin/python realtime_analyzer.py --model models/threat_detector.joblib
# Press Ctrl+C after a few seconds to stop
```

---

### Problem: "Dashboard not updating"
**Solutions:**
1. Enable "Auto-Refresh" toggle in sidebar
2. Check if `data/ml_predictions.json` file exists and is being updated
3. Manually refresh the page (F5)

---

## 🎯 QUICK TEST SEQUENCE

### Full System Test (5 minutes):

1. **Launch Dashboard:**
   ```bash
   ./launch_complete.sh
   ```

2. **Open Browser:**
   - Go to: http://localhost:8501

3. **Train Model:**
   - Sidebar → Click "🎓 Train ML Model"
   - Wait for success message

4. **Generate Sample Data:**
   - Sidebar → Click "📊 Generate Sample Data"
   - Verify data appears in tabs

5. **Start Real-Time Analyzer:**
   - Sidebar → Click "▶️ Start Real-Time Analyzer"
   - Enter sudo password
   - Wait for success message

6. **Enable Auto-Refresh:**
   - Sidebar → Toggle "🔄 Auto-Refresh Dashboard" ON

7. **Generate Traffic (in another terminal):**
   ```bash
   # Open new terminal
   ping -c 50 google.com &
   curl -s https://httpbin.org/ip
   ```

8. **Watch Dashboard:**
   - Go to "📡 Live Monitoring" tab
   - You should see packets appearing
   - Go to "🤖 ML Predictions" tab
   - You should see predictions

9. **Verify in Terminal:**
   ```bash
   # Check files are updating
   watch -n 2 'ls -lth data/*.json | head -3'
   ```

---

## 📊 EXPECTED BEHAVIOR

### Normal Operation:
- **Dashboard:** Updates every 3 seconds (if auto-refresh enabled)
- **Analyzer:** Captures packets continuously
- **Predictions:** Generated every 5 seconds (window size)
- **Files:** `ml_predictions.json` and `ml_stats.json` updated every 5s

### Performance Indicators:
- ✅ **CPU Usage:** 5-15% (normal)
- ✅ **Memory:** 100-200MB (analyzer + dashboard)
- ✅ **Response Time:** < 1 second for dashboard refresh

---

## 🔧 MANUAL VERIFICATION COMMANDS

### Check Process Status:
```bash
# All running processes
ps aux | grep -E "(streamlit|realtime|python)" | grep -v grep
```

### Check File Timestamps:
```bash
# Most recent files
ls -lth data/ | head -10
```

### Check File Sizes:
```bash
# Growing files indicate activity
watch -n 2 'du -h data/*.json data/*.csv'
```

### Monitor Live Updates:
```bash
# Watch predictions file
watch -n 1 'tail -20 data/ml_predictions.json'
```

### Check Network Activity:
```bash
# Monitor network interfaces
sudo iftop -i any
# (Press Ctrl+C to stop)
```

---

## ✅ SUCCESS INDICATORS

You know everything is working when:

1. ✅ Dashboard loads at http://localhost:8501
2. ✅ "Real-Time Analyzer Status: 🟢 Running" in sidebar
3. ✅ "ML Model Status: ✅ Loaded" in sidebar
4. ✅ Auto-refresh counter is counting down
5. ✅ Live Monitoring tab shows recent packets
6. ✅ ML Predictions tab shows new predictions
7. ✅ Statistics tab shows charts with data
8. ✅ Files `ml_predictions.json` and `ml_stats.json` update every 5s
9. ✅ Packet count increases in Overview tab
10. ✅ No error messages in browser console

---

## 🎉 YOU'RE ALL SET!

If you see these indicators, **your NetGuard AI is working perfectly**:
- 🟢 Analyzer capturing packets
- 🤖 ML model making predictions
- 📊 Dashboard updating automatically
- ⚠️ Threats being detected and logged

---

## 📞 STILL HAVING ISSUES?

### Last Resort Debug Commands:

```bash
# Kill everything and restart
pkill -f streamlit
pkill -f realtime_analyzer

# Start fresh
./launch_complete.sh
```

### Check Logs:
```bash
# Look for error messages
tail -50 data/threat_logs.json
```

### Test Without Sudo (won't capture, but tests everything else):
```bash
# This will fail to capture but shows if code works
.venv/bin/python realtime_analyzer.py --model models/threat_detector.joblib
```

---

## 🚀 QUICK REFERENCE

| What to Check | Command | Expected Result |
|---------------|---------|-----------------|
| Dashboard running | `ps aux \| grep streamlit` | Process found |
| Analyzer running | `ps aux \| grep realtime` | Process found |
| Files updating | `ls -lth data/*.json` | Recent timestamps |
| Network traffic | `sudo tcpdump -i any -c 10` | Packets captured |
| Model exists | `ls -lh models/*.joblib` | File exists |

---

**Remember:** The analyzer needs **sudo permissions** to capture network packets!
