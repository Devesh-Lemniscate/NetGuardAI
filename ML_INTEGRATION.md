# 🤖 Real-Time ML Integration Guide

## ✅ What's Been Added

Your NetGuard AI now has a complete **real-time ML-based threat detection pipeline**!

### New Components:

1. **`realtime_analyzer.py`** - Complete real-time analysis pipeline
   - Continuous packet capture in 5-second windows
   - Automatic feature extraction (27+ features)
   - ML-based threat prediction
   - Thread-safe queue for dashboard integration

2. **`train_model.py`** - ML model training script
   - Trains Random Forest classifier
   - Generates synthetic training data
   - Saves model to `models/threat_detector.joblib`

---

## 🚀 Quick Start - Real-Time ML Detection

### Step 1: Train the ML Model (First Time Only)
```bash
.venv/bin/python train_model.py
```
This creates `models/threat_detector.joblib`

### Step 2: Run Real-Time Analysis
```bash
# Without ML model (uses rule-based detection)
sudo .venv/bin/python realtime_analyzer.py

# With ML model
sudo .venv/bin/python realtime_analyzer.py --model models/threat_detector.joblib

# Custom window size (default is 5 seconds)
sudo .venv/bin/python realtime_analyzer.py --window 10 --model models/threat_detector.joblib

# Specific network interface
sudo .venv/bin/python realtime_analyzer.py --interface eth0 --model models/threat_detector.joblib
```

---

## 📊 How It Works

### Architecture:

```
┌─────────────────┐
│ Packet Capture  │  (Continuous, Thread 1)
│    (Scapy)      │
└────────┬────────┘
         │ Packets stored in buffer
         ↓
┌─────────────────┐
│ Time Window     │  Every 5 seconds
│  (5 seconds)    │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│ Feature Extract │  27+ aggregated features
│  - Packet count │  - Protocol distribution
│  - Byte stats   │  - Port analysis
│  - Entropy      │  - Flow patterns
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  ML Prediction  │  Random Forest / XGBoost
│ (or Rule-based) │  Confidence score
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│ Prediction Queue│  Thread-safe queue
│  (Dashboard)    │  Latest predictions
└─────────────────┘
```

### Features Extracted (27 total):
- **Packet Statistics**: Count, unique IPs, unique ports
- **Byte Statistics**: Total, mean, max, min, std
- **Protocol Distribution**: TCP, UDP, ICMP counts
- **Port Analysis**: HTTP, HTTPS, DNS, SSH traffic
- **TTL Features**: Mean, min, max TTL values
- **Time Features**: Duration, packets per second
- **Entropy**: Source/destination IP entropy
- **Flow Patterns**: Max IP counts, distribution

---

## 🔧 Integration with Existing System

### Using Real-Time Analyzer in Your Code:

```python
from realtime_analyzer import RealTimeAnalyzer
import time

# Create analyzer
analyzer = RealTimeAnalyzer(
    window_size=5,  # 5-second windows
    model_path='models/threat_detector.joblib'  # Optional
)

# Start analysis
analyzer.start(interface=None)  # Use default interface

try:
    while True:
        # Get latest prediction
        prediction = analyzer.get_latest_prediction()
        
        if prediction:
            print(f"Threat: {prediction['is_threat']}")
            print(f"Type: {prediction['threat_type']}")
            print(f"Confidence: {prediction['confidence']:.2%}")
        
        # Get statistics
        stats = analyzer.get_statistics()
        print(f"Packets captured: {stats['total_packets']}")
        
        time.sleep(1)

except KeyboardInterrupt:
    analyzer.stop()
```

---

## 🎯 Comparison: Old vs New System

### Old System (Rule-Based):
- ✅ Simple port scan detection
- ✅ Basic DoS detection
- ❌ Limited feature analysis
- ❌ No ML capabilities
- ❌ Fixed thresholds

### New System (ML-Enhanced):
- ✅ **27+ aggregated features**
- ✅ **ML-based classification**
- ✅ **Confidence scores**
- ✅ **Continuous learning ready**
- ✅ **Real-time windows (5s)**
- ✅ **Thread-safe architecture**
- ✅ **Dashboard integration ready**
- ✅ **Graceful shutdown (Ctrl+C)**

---

## 📝 Commands Reference

### Train Model:
```bash
.venv/bin/python train_model.py
```

### Run Real-Time Analyzer:
```bash
# Basic (rule-based)
sudo .venv/bin/python realtime_analyzer.py

# With ML model
sudo .venv/bin/python realtime_analyzer.py --model models/threat_detector.joblib

# Custom settings
sudo .venv/bin/python realtime_analyzer.py \
    --model models/threat_detector.joblib \
    --window 10 \
    --interface wlan0
```

### Check Available Interfaces:
```bash
ip link show
```

---

## 🔍 What Gets Logged

### Normal Traffic:
```
✅ Normal traffic (packets: 45, bytes: 23450)
```

### Threat Detected:
```
⚠️ THREAT DETECTED: port_scan_detected (confidence: 85.43%)
⚠️ THREAT DETECTED: ml_detected_threat (confidence: 92.17%)
```

### Statistics (every 10s):
```
📊 Stats - Packets: 1234, Predictions: 24, Threats: 3
```

---

## 🛡️ Integration with Dashboard

The dashboard can access real-time predictions through the queue:

```python
# In dashboard code
from realtime_analyzer import RealTimeAnalyzer

# Global analyzer instance
analyzer = RealTimeAnalyzer(window_size=5, model_path='models/threat_detector.joblib')
analyzer.start()

# Get predictions in dashboard
def get_realtime_threats():
    predictions = []
    while not analyzer.prediction_queue.empty():
        pred = analyzer.get_latest_prediction()
        if pred:
            predictions.append(pred)
    return predictions
```

---

## ⚙️ Configuration Options

### Window Size:
- **Small (1-3s)**: More frequent predictions, higher CPU
- **Medium (5-10s)**: Balanced (recommended)
- **Large (15-30s)**: Better feature aggregation, slower response

### Model Options:
- **No model**: Uses rule-based detection
- **Random Forest**: Good accuracy, fast
- **XGBoost**: Better accuracy, slightly slower (future)

---

## 🧪 Testing the System

### 1. Generate Training Data and Train Model:
```bash
.venv/bin/python train_model.py
```

### 2. Run Analyzer (in one terminal):
```bash
sudo .venv/bin/python realtime_analyzer.py --model models/threat_detector.joblib
```

### 3. Generate Network Traffic (in another terminal):
```bash
# Ping test
ping -c 100 google.com

# Web traffic
curl -s https://example.com > /dev/null

# Multiple connections
for i in {1..50}; do curl -s https://httpbin.org/ip & done
```

### 4. Watch for Detections:
The analyzer will log any threats detected in real-time.

---

## 🔐 Security Notes

- **Requires root/sudo** for packet capture
- **Network interface access** needed
- **CPU usage** depends on traffic volume
- **Memory usage** capped by buffer size (10,000 packets)

---

## 🎓 Advanced Usage

### Custom Feature Engineering:
Edit `realtime_analyzer.py` → `extract_flow_features()` to add your own features.

### Custom ML Model:
Train your own model with real data:
```python
import joblib
from sklearn.ensemble import RandomForestClassifier

# Load your labeled data
X_train, y_train = load_your_data()

# Train
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

# Save
joblib.dump(model, 'models/my_custom_model.joblib')
```

### Multiple Interfaces:
Run multiple analyzers for different interfaces:
```bash
# Terminal 1
sudo .venv/bin/python realtime_analyzer.py --interface eth0

# Terminal 2
sudo .venv/bin/python realtime_analyzer.py --interface wlan0
```

---

## ✅ Verification Checklist

- [x] Real-time packet capture (continuous)
- [x] Time-windowed feature extraction (5s windows)
- [x] ML model integration (Random Forest)
- [x] Thread-safe prediction queue
- [x] Graceful shutdown (Ctrl+C)
- [x] Dashboard integration ready
- [x] Modular architecture
- [x] Rule-based fallback
- [x] Comprehensive logging
- [x] Statistics tracking

---

## 🎉 You Now Have:

1. ✅ **Continuous packet capture** with scapy
2. ✅ **27+ aggregated features** extracted every 5 seconds
3. ✅ **ML-based threat prediction** with confidence scores
4. ✅ **Thread-safe queue** for dashboard integration
5. ✅ **Runs indefinitely** until Ctrl+C
6. ✅ **Graceful shutdown** handling
7. ✅ **Modular, clean code** architecture
8. ✅ **Complete documentation**

**Your site still works perfectly** - the old system is untouched!

---

## 🚀 Next Steps:

1. Train the model: `.venv/bin/python train_model.py`
2. Run real-time analysis: `sudo .venv/bin/python realtime_analyzer.py --model models/threat_detector.joblib`
3. Watch the magic happen! 🎩✨

**The dashboard integration is ready - just import RealTimeAnalyzer!**
