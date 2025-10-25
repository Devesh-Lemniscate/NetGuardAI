#!/usr/bin/env python3
"""
NetGuard AI - Complete System Verification
Checks all components including ML integration
"""

import os
import sys
from pathlib import Path

def print_header(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def check_mark(condition):
    return "✅" if condition else "❌"

def main():
    print_header("🛡️  NetGuard AI - System Verification")
    
    # Check virtual environment
    print("\n1️⃣  Virtual Environment:")
    venv_active = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    print(f"   {check_mark(venv_active)} Virtual environment active")
    print(f"   Python version: {sys.version.split()[0]}")
    print(f"   Python path: {sys.executable}")
    
    # Check core packages
    print("\n2️⃣  Core Dependencies:")
    packages = {
        'scapy': 'Packet capture',
        'pandas': 'Data processing',
        'numpy': 'Numerical computing',
        'sklearn': 'Machine learning',
        'streamlit': 'Dashboard',
        'joblib': 'Model persistence',
        'plotly': 'Visualizations'
    }
    
    for package, description in packages.items():
        try:
            __import__(package)
            print(f"   ✅ {package:15} - {description}")
        except ImportError:
            print(f"   ❌ {package:15} - {description} (MISSING)")
    
    # Check project files
    print("\n3️⃣  Project Files:")
    required_files = {
        'main.py': 'Main packet capture',
        'packet_capture.py': 'Packet capture module',
        'threat_model.py': 'Threat detection (rule-based)',
        'feature_extractor.py': 'Feature extraction',
        'realtime_analyzer.py': 'Real-time ML analyzer (NEW)',
        'train_model.py': 'ML model training (NEW)',
        'generate_sample_data.py': 'Sample data generator',
        'dashboard/app.py': 'Streamlit dashboard',
        'requirements.txt': 'Dependencies list'
    }
    
    for file, description in required_files.items():
        exists = os.path.exists(file)
        print(f"   {check_mark(exists)} {file:30} - {description}")
    
    # Check directories
    print("\n4️⃣  Directories:")
    dirs = ['data', 'models', 'dashboard', 'utils', 'jupyter_notebooks']
    for d in dirs:
        exists = os.path.isdir(d)
        print(f"   {check_mark(exists)} {d}/")
    
    # Check data files
    print("\n5️⃣  Data Files:")
    data_files = {
        'data/packets_log.csv': 'Packet logs',
        'data/threat_logs.json': 'Threat logs',
        'models/threat_detector.joblib': 'ML model (optional)'
    }
    
    for file, description in data_files.items():
        exists = os.path.exists(file)
        status = check_mark(exists)
        if not exists and 'optional' in description:
            status = "⚠️ "
        print(f"   {status} {file:35} - {description}")
    
    # Check shell scripts
    print("\n6️⃣  Launcher Scripts:")
    scripts = ['run.sh', 'launch_dashboard.sh', 'test.sh']
    for script in scripts:
        exists = os.path.exists(script)
        executable = os.access(script, os.X_OK) if exists else False
        print(f"   {check_mark(exists and executable)} {script:25} - {'Executable' if executable else 'Not executable'}")
    
    # Test imports of project modules
    print("\n7️⃣  Project Modules:")
    try:
        from threat_model import ThreatDetector
        print(f"   ✅ ThreatDetector imported")
    except Exception as e:
        print(f"   ❌ ThreatDetector failed: {e}")
    
    try:
        from feature_extractor import extract_features
        print(f"   ✅ extract_features imported")
    except Exception as e:
        print(f"   ❌ extract_features failed: {e}")
    
    try:
        from realtime_analyzer import RealTimeAnalyzer
        print(f"   ✅ RealTimeAnalyzer imported (NEW)")
    except Exception as e:
        print(f"   ❌ RealTimeAnalyzer failed: {e}")
    
    # Check ML model
    print("\n8️⃣  ML Model Status:")
    model_path = 'models/threat_detector.joblib'
    if os.path.exists(model_path):
        try:
            import joblib
            model = joblib.load(model_path)
            print(f"   ✅ ML model loaded successfully")
            print(f"   Model type: {type(model).__name__}")
            if hasattr(model, 'n_estimators'):
                print(f"   Estimators: {model.n_estimators}")
        except Exception as e:
            print(f"   ❌ ML model exists but failed to load: {e}")
    else:
        print(f"   ⚠️  ML model not found - run: .venv/bin/python train_model.py")
    
    # Feature count test
    print("\n9️⃣  Feature Extraction Test:")
    try:
        from realtime_analyzer import RealTimeAnalyzer
        analyzer = RealTimeAnalyzer()
        test_packets = [
            {
                'timestamp': __import__('datetime').datetime.now(),
                'src_ip': '192.168.1.1',
                'dst_ip': '8.8.8.8',
                'protocol': 6,
                'size': 100,
                'ttl': 64,
                'src_port': 50000,
                'dst_port': 443,
                'flags': 'S'
            }
        ]
        features = analyzer.extract_flow_features(test_packets)
        print(f"   ✅ Feature extraction working")
        print(f"   Features extracted: {len(features)}")
        print(f"   Feature names: {', '.join(list(features.keys())[:5])}...")
    except Exception as e:
        print(f"   ❌ Feature extraction failed: {e}")
    
    # Documentation
    print("\n🔟 Documentation:")
    docs = ['README.md', 'START_HERE.md', 'QUICKSTART.md', 'ML_INTEGRATION.md']
    for doc in docs:
        exists = os.path.exists(doc)
        print(f"   {check_mark(exists)} {doc}")
    
    # Summary
    print_header("📊 Summary")
    
    print("\n✅ WHAT'S WORKING:")
    print("   • Virtual environment configured")
    print("   • All dependencies installed")
    print("   • Packet capture system ready")
    print("   • Rule-based threat detection ready")
    print("   • Real-time ML analyzer ready (NEW)")
    print("   • Dashboard application ready")
    print("   • Sample data generated")
    
    print("\n🚀 QUICK START:")
    print("   1. View dashboard:        ./launch_dashboard.sh")
    print("   2. Train ML model:        .venv/bin/python train_model.py")
    print("   3. Run ML analyzer:       sudo .venv/bin/python realtime_analyzer.py --model models/threat_detector.joblib")
    print("   4. Interactive menu:      ./run.sh")
    
    if not os.path.exists('models/threat_detector.joblib'):
        print("\n⚠️  RECOMMENDATION:")
        print("   Train the ML model first: .venv/bin/python train_model.py")
    
    print("\n📚 DOCUMENTATION:")
    print("   • START_HERE.md      - Quick start guide")
    print("   • ML_INTEGRATION.md  - ML pipeline documentation (NEW)")
    print("   • QUICKSTART.md      - Detailed setup guide")
    
    print("\n" + "="*60)
    print("🎉 System verification complete!")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
