#!/usr/bin/env python3
"""
Integrated launcher for NetGuard AI
Runs ML analyzer and dashboard together
"""

import subprocess
import time
import sys
import os
import signal
from pathlib import Path

# Color codes
GREEN = '\033[0;32m'
BLUE = '\033[0;34m'
YELLOW = '\033[1;33m'
RED = '\033[0;31m'
NC = '\033[0m'  # No Color

def print_banner():
    print("╔══════════════════════════════════════════════════════════╗")
    print("║     🛡️  NetGuard AI - Integrated Launch System          ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print()

def check_requirements():
    """Check if ML model exists"""
    model_path = Path("models/threat_detector.joblib")
    if not model_path.exists():
        print(f"{YELLOW}⚠️  ML model not found!{NC}")
        print(f"   Run: .venv/bin/python train_model.py")
        print()
        response = input("Continue without ML model? (y/n): ")
        if response.lower() != 'y':
            sys.exit(1)
        return None
    return str(model_path)

def run_analyzer(model_path=None, interface=None):
    """Run the ML analyzer in background"""
    cmd = ["sudo", ".venv/bin/python", "realtime_analyzer.py"]
    
    if model_path:
        cmd.extend(["--model", model_path])
    
    if interface:
        cmd.extend(["--interface", interface])
    
    print(f"{BLUE}📡 Starting ML Analyzer...{NC}")
    print(f"   Command: {' '.join(cmd)}")
    print()
    
    # Start analyzer
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )
    
    return process

def run_dashboard():
    """Run the dashboard"""
    print(f"{BLUE}🎨 Starting Dashboard...{NC}")
    print(f"   Dashboard will be available at: http://localhost:8501")
    print()
    
    # Change to dashboard directory and run
    cmd = ["../.venv/bin/streamlit", "run", "app_realtime.py", 
           "--server.headless", "true"]
    
    process = subprocess.Popen(
        cmd,
        cwd="dashboard",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )
    
    return process

def main():
    print_banner()
    
    # Check sudo
    if os.geteuid() != 0:
        print(f"{RED}❌ This script requires sudo privileges for packet capture{NC}")
        print(f"   Run: sudo .venv/bin/python launch_integrated.py")
        sys.exit(1)
    
    # Check model
    model_path = check_requirements()
    
    # Ask for network interface
    print(f"{BLUE}Network Interface:{NC}")
    print("  Leave blank for default interface")
    print("  Or specify: eth0, wlan0, etc.")
    interface = input("Interface (optional): ").strip() or None
    print()
    
    print(f"{GREEN}🚀 Launching NetGuard AI...{NC}")
    print()
    
    # Start analyzer
    analyzer_process = run_analyzer(model_path, interface)
    
    # Wait a bit for analyzer to start
    print("   Waiting for analyzer to initialize...")
    time.sleep(3)
    
    # Start dashboard
    dashboard_process = run_dashboard()
    
    # Wait for dashboard to start
    print("   Waiting for dashboard to start...")
    time.sleep(5)
    
    print()
    print(f"{GREEN}✅ System is running!{NC}")
    print()
    print("="*60)
    print(f"📡 ML Analyzer: Running (PID: {analyzer_process.pid})")
    print(f"🎨 Dashboard: http://localhost:8501")
    print("="*60)
    print()
    print(f"{YELLOW}Press Ctrl+C to stop both services{NC}")
    print()
    
    # Monitor processes
    try:
        while True:
            # Check if processes are still running
            analyzer_running = analyzer_process.poll() is None
            dashboard_running = dashboard_process.poll() is None
            
            if not analyzer_running:
                print(f"{RED}❌ Analyzer stopped unexpectedly{NC}")
                break
            
            if not dashboard_running:
                print(f"{RED}❌ Dashboard stopped unexpectedly{NC}")
                break
            
            time.sleep(1)
    
    except KeyboardInterrupt:
        print()
        print(f"{YELLOW}🛑 Stopping services...{NC}")
    
    finally:
        # Cleanup
        print("   Terminating analyzer...")
        try:
            analyzer_process.terminate()
            analyzer_process.wait(timeout=5)
        except:
            analyzer_process.kill()
        
        print("   Terminating dashboard...")
        try:
            dashboard_process.terminate()
            dashboard_process.wait(timeout=5)
        except:
            dashboard_process.kill()
        
        print(f"{GREEN}✅ Services stopped cleanly{NC}")
        print()
        print("👋 Goodbye!")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"{RED}❌ Error: {e}{NC}")
        sys.exit(1)
