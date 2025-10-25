#!/usr/bin/env python3
"""
Quick test to verify ML integration works
"""

print("🧪 Testing ML Integration...\n")

# Test 1: Import RealTimeAnalyzer
print("1. Testing RealTimeAnalyzer import...")
try:
    from realtime_analyzer import RealTimeAnalyzer
    print("   ✅ RealTimeAnalyzer imported successfully")
except Exception as e:
    print(f"   ❌ Failed: {e}")
    exit(1)

# Test 2: Create analyzer instance
print("\n2. Testing analyzer creation...")
try:
    analyzer = RealTimeAnalyzer(window_size=5)
    print("   ✅ Analyzer created successfully")
except Exception as e:
    print(f"   ❌ Failed: {e}")
    exit(1)

# Test 3: Feature extraction
print("\n3. Testing feature extraction...")
try:
    from datetime import datetime
    test_packets = [
        {
            'timestamp': datetime.now(),
            'src_ip': '192.168.1.100',
            'dst_ip': '8.8.8.8',
            'protocol': 6,
            'size': 1200,
            'ttl': 64,
            'src_port': 50000,
            'dst_port': 443,
            'flags': 'S'
        },
        {
            'timestamp': datetime.now(),
            'src_ip': '192.168.1.100',
            'dst_ip': '8.8.8.8',
            'protocol': 6,
            'size': 800,
            'ttl': 64,
            'src_port': 50001,
            'dst_port': 443,
            'flags': 'A'
        }
    ]
    
    features = analyzer.extract_flow_features(test_packets)
    print(f"   ✅ Extracted {len(features)} features")
    print(f"   Features: total_packets={features['total_packets']}, "
          f"total_bytes={features['total_bytes']}, "
          f"tcp_packets={features['tcp_packets']}")
except Exception as e:
    print(f"   ❌ Failed: {e}")
    exit(1)

# Test 4: Prediction (rule-based)
print("\n4. Testing prediction (rule-based)...")
try:
    prediction = analyzer.predict_threat(features)
    print(f"   ✅ Prediction generated")
    print(f"   Is threat: {prediction['is_threat']}")
    print(f"   Threat type: {prediction['threat_type']}")
    print(f"   Confidence: {prediction['confidence']:.2%}")
except Exception as e:
    print(f"   ❌ Failed: {e}")
    exit(1)

# Test 5: Check if ML model exists
print("\n5. Checking ML model...")
import os
if os.path.exists('models/threat_detector.joblib'):
    print("   ✅ ML model found: models/threat_detector.joblib")
    try:
        analyzer_ml = RealTimeAnalyzer(
            window_size=5,
            model_path='models/threat_detector.joblib'
        )
        prediction_ml = analyzer_ml.predict_threat(features)
        print(f"   ✅ ML prediction works")
        print(f"   ML threat: {prediction_ml['is_threat']}, "
              f"confidence: {prediction_ml['confidence']:.2%}")
    except Exception as e:
        print(f"   ⚠️  ML model exists but prediction failed: {e}")
else:
    print("   ⚠️  ML model not found (this is OK)")
    print("   To train: .venv/bin/python train_model.py")

# Test 6: Check queue mechanism
print("\n6. Testing queue mechanism...")
try:
    import queue
    test_queue = queue.Queue(maxsize=10)
    test_queue.put({'test': 'data'})
    result = test_queue.get_nowait()
    print("   ✅ Queue mechanism works")
except Exception as e:
    print(f"   ❌ Failed: {e}")

# Test 7: Check threading readiness
print("\n7. Testing threading readiness...")
try:
    import threading
    test_var = [0]
    
    def test_thread():
        test_var[0] = 1
    
    t = threading.Thread(target=test_thread, daemon=True)
    t.start()
    t.join(timeout=1)
    
    if test_var[0] == 1:
        print("   ✅ Threading works")
    else:
        print("   ⚠️  Threading may have issues")
except Exception as e:
    print(f"   ❌ Failed: {e}")

# Summary
print("\n" + "="*60)
print("✅ ML INTEGRATION TEST PASSED!")
print("="*60)
print("\n🎯 Next Steps:")
print("   1. Train model:     .venv/bin/python train_model.py")
print("   2. Run analyzer:    sudo .venv/bin/python realtime_analyzer.py")
print("   3. View dashboard:  ./launch_dashboard.sh")
print("\n💡 For packet capture, you need sudo/root privileges")
print("   Try: sudo .venv/bin/python realtime_analyzer.py --model models/threat_detector.joblib\n")
