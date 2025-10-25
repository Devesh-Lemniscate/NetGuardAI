"""
🛡️ NetGuard AI - Complete Feature Dashboard
All-in-one interface for packet capture, ML detection, threat analysis, and system control
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import os
import sys
from datetime import datetime, timedelta
import time
from pathlib import Path
import subprocess
import signal
from collections import defaultdict

# Add parent directory to path
sys.path.insert(0, os.path.abspath('..'))

# Page configuration
st.set_page_config(
    page_title="🛡️ NetGuard AI - Complete Dashboard", 
    page_icon="🛡️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .threat-alert {
        padding: 20px;
        background-color: #ff4444;
        color: white;
        border-radius: 10px;
        font-weight: bold;
        font-size: 20px;
        text-align: center;
        animation: pulse 1s infinite;
        margin: 10px 0;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    .normal-status {
        padding: 20px;
        background-color: #44ff44;
        color: #006600;
        border-radius: 10px;
        font-weight: bold;
        font-size: 20px;
        text-align: center;
        margin: 10px 0;
    }
    
    .feature-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin: 10px 0;
        cursor: pointer;
        transition: transform 0.2s;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
    }
    
    .info-box {
        background-color: #e3f2fd;
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #2196f3;
        margin: 10px 0;
    }
    
    .success-box {
        background-color: #e8f5e9;
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #4caf50;
        margin: 10px 0;
    }
    
    .warning-box {
        background-color: #fff3e0;
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #ff9800;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# File paths
PACKETS_LOG = "../data/packets_log.csv"
THREATS_LOG = "../data/threat_logs.json"
ML_PREDICTIONS_LOG = "../data/ml_predictions.json"
ML_STATS_LOG = "../data/ml_stats.json"
MODEL_PATH = "../models/threat_detector.joblib"

# Initialize session state
if 'analyzer_running' not in st.session_state:
    st.session_state.analyzer_running = False
if 'analyzer_pid' not in st.session_state:
    st.session_state.analyzer_pid = None
if 'last_refresh' not in st.session_state:
    st.session_state.last_refresh = datetime.now()

def load_packet_data():
    """Load packet capture data"""
    if os.path.exists(PACKETS_LOG):
        try:
            df = pd.read_csv(PACKETS_LOG)
            if not df.empty:
                df['Timestamp'] = pd.to_datetime(df['Timestamp'])
                return df
        except Exception as e:
            st.error(f"Error loading packet data: {e}")
    return pd.DataFrame()

def load_threat_data():
    """Load threat detection data"""
    if os.path.exists(THREATS_LOG):
        try:
            with open(THREATS_LOG, 'r') as f:
                return json.load(f)
        except Exception as e:
            st.error(f"Error loading threat data: {e}")
    return []

def load_ml_predictions():
    """Load ML prediction data"""
    if os.path.exists(ML_PREDICTIONS_LOG):
        try:
            with open(ML_PREDICTIONS_LOG, 'r') as f:
                return json.load(f)
        except Exception as e:
            pass
    return []

def load_ml_stats():
    """Load ML statistics"""
    if os.path.exists(ML_STATS_LOG):
        try:
            with open(ML_STATS_LOG, 'r') as f:
                return json.load(f)
        except Exception as e:
            pass
    return {}

def check_model_exists():
    """Check if ML model exists"""
    return os.path.exists(MODEL_PATH)

def train_model():
    """Train the ML model"""
    try:
        # Get absolute paths
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        python_path = os.path.join(base_dir, '.venv', 'bin', 'python')
        train_script = os.path.join(base_dir, 'train_model.py')
        
        result = subprocess.run(
            [python_path, train_script],
            capture_output=True,
            text=True,
            cwd=base_dir
        )
        return result.returncode == 0, result.stdout + result.stderr
    except Exception as e:
        return False, str(e)

def start_analyzer():
    """Start the real-time analyzer"""
    try:
        # Get absolute paths
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        python_path = os.path.join(base_dir, '.venv', 'bin', 'python')
        analyzer_script = os.path.join(base_dir, 'realtime_analyzer.py')
        model_path = os.path.join(base_dir, 'models', 'threat_detector.joblib')
        log_file = os.path.join(base_dir, 'data', 'analyzer.log')
        
        # Auto-detect active network interface (prefer wlo1, eth0, or eno1)
        interface = None
        try:
            result = subprocess.run(['ip', '-br', 'link'], capture_output=True, text=True)
            for line in result.stdout.split('\n'):
                if 'UP' in line and not line.startswith('lo'):
                    interface = line.split()[0]
                    if interface in ['wlo1', 'wlan0', 'eth0', 'eno1']:
                        break
        except:
            pass
        
        cmd = ['sudo', '-S', python_path, analyzer_script]
        if os.path.exists(model_path):
            cmd.extend(['--model', model_path])
        if interface:
            cmd.extend(['--interface', interface])
        
        # Start process in background with output redirected to log file
        log_f = open(log_file, 'w')
        process = subprocess.Popen(
            cmd,
            stdout=log_f,
            stderr=subprocess.STDOUT,
            stdin=subprocess.PIPE,
            cwd=base_dir,
            start_new_session=True
        )
        
        st.session_state.analyzer_pid = process.pid
        st.session_state.analyzer_running = True
        msg = f"Analyzer started with PID: {process.pid}"
        if interface:
            msg += f" on interface {interface}"
        msg += f"\nCheck logs at: {log_file}"
        return True, msg
    except Exception as e:
        return False, str(e)

def stop_analyzer():
    """Stop the real-time analyzer"""
    try:
        if st.session_state.analyzer_pid:
            os.kill(st.session_state.analyzer_pid, signal.SIGINT)
            st.session_state.analyzer_running = False
            st.session_state.analyzer_pid = None
            return True, "Analyzer stopped successfully"
        else:
            return False, "No analyzer process running"
    except Exception as e:
        return False, str(e)

def generate_sample_data():
    """Generate sample test data"""
    try:
        # Get absolute paths
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        python_path = os.path.join(base_dir, '.venv', 'bin', 'python')
        
        # Generate packets
        result1 = subprocess.run(
            [python_path, '-c', 
             'from utils.data_preprocess import generate_sample_data; generate_sample_data(num_packets=100)'],
            capture_output=True,
            text=True,
            cwd=base_dir
        )
        
        # Generate threats
        result2 = subprocess.run(
            [python_path, '-c',
             'from utils.data_preprocess import generate_sample_threats; generate_sample_threats(num_threats=20)'],
            capture_output=True,
            text=True,
            cwd=base_dir
        )
        
        success = result1.returncode == 0 and result2.returncode == 0
        return success, "Sample data generated successfully" if success else "Error generating data"
    except Exception as e:
        return False, str(e)

# ==================== MAIN DASHBOARD ====================

# Header
st.markdown("<h1 style='text-align: center; color: #667eea;'>🛡️ NetGuard AI - Complete Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666;'>Real-Time Network Threat Detection & Analysis Platform</p>", unsafe_allow_html=True)
st.markdown("---")

# Sidebar - System Control
with st.sidebar:
    st.markdown("## 🎛️ System Control")
    
    # Model Status
    model_exists = check_model_exists()
    if model_exists:
        st.success("✅ ML Model Ready")
    else:
        st.warning("⚠️ ML Model Not Found")
    
    st.markdown("---")
    
    # Train Model
    st.markdown("### 🤖 ML Model Training")
    if st.button("🎓 Train ML Model", width="stretch"):
        with st.spinner("Training model... This may take a minute..."):
            success, msg = train_model()
            if success:
                st.success("✅ Model trained successfully!")
            else:
                st.error(f"❌ Training failed: {msg}")
    
    st.markdown("---")
    
    # Analyzer Control
    st.markdown("### 🔄 Real-Time Analyzer")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("▶️ Start", width="stretch", disabled=st.session_state.analyzer_running):
            success, msg = start_analyzer()
            if success:
                st.success(msg)
            else:
                st.error(f"Error: {msg}")
    
    with col2:
        if st.button("⏹️ Stop", width="stretch", disabled=not st.session_state.analyzer_running):
            success, msg = stop_analyzer()
            if success:
                st.success(msg)
            else:
                st.error(f"Error: {msg}")
    
    if st.session_state.analyzer_running:
        st.info(f"🟢 Running (PID: {st.session_state.analyzer_pid})")
    else:
        st.info("🔴 Stopped")
    
    st.markdown("---")
    
    # Generate Sample Data
    st.markdown("### 🧪 Test Data")
    if st.button("📊 Generate Sample Data", width="stretch"):
        with st.spinner("Generating..."):
            success, msg = generate_sample_data()
            if success:
                st.success(msg)
            else:
                st.error(msg)
    
    st.markdown("---")
    
    # Refresh Control
    st.markdown("### 🔄 Auto-Refresh")
    auto_refresh = st.checkbox("Enable Auto-Refresh", value=True)
    refresh_interval = st.slider("Interval (seconds)", 1, 10, 2)
    
    if st.button("🔄 Manual Refresh", width="stretch"):
        st.rerun()

# Main Content Tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Overview",
    "🔍 Live Monitoring", 
    "🤖 ML Predictions",
    "🚨 Threat Analysis",
    "📈 Statistics",
    "ℹ️ Features & Guide"
])

# ==================== TAB 1: OVERVIEW ====================
with tab1:
    st.markdown("## 📊 System Overview")
    
    # Load data
    packets_df = load_packet_data()
    threats = load_threat_data()
    ml_predictions = load_ml_predictions()
    ml_stats = load_ml_stats()
    
    # Top metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_packets = len(packets_df) if not packets_df.empty else 0
        st.metric("📦 Total Packets", f"{total_packets:,}")
    
    with col2:
        # All entries in threat_logs.json are threats (no 'threat' key needed)
        total_threats = len([t for t in threats if t.get('threat', True)])
        st.metric("🚨 Threats Detected", total_threats)
    
    with col3:
        ml_windows = ml_stats.get('windows_processed', 0) if ml_stats else 0
        st.metric("🔍 Windows Analyzed", ml_windows)
    
    with col4:
        ml_threat_count = ml_stats.get('threat_count', 0) if ml_stats else 0
        st.metric("🤖 ML Threats", ml_threat_count)
    
    st.markdown("---")
    
    # Quick Status
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔧 System Status")
        status_data = {
            "Component": ["Virtual Environment", "ML Model", "Real-Time Analyzer", "Data Logs"],
            "Status": [
                "✅ Active" if os.path.exists("../.venv") else "❌ Missing",
                "✅ Ready" if model_exists else "⚠️ Not Trained",
                "🟢 Running" if st.session_state.analyzer_running else "🔴 Stopped",
                "✅ Available" if os.path.exists(PACKETS_LOG) else "⚠️ No Data"
            ]
        }
        st.dataframe(pd.DataFrame(status_data), width="stretch", hide_index=True)
    
    with col2:
        st.markdown("### 📊 Data Summary")
        if not packets_df.empty:
            recent_packets = packets_df.tail(100)
            protocol_dist = recent_packets['Protocol'].value_counts()
            
            fig = px.pie(
                values=protocol_dist.values,
                names=protocol_dist.index,
                title="Recent Traffic by Protocol",
                hole=0.4
            )
            st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
        else:
            st.info("No packet data available. Generate sample data or start the analyzer.")
    
    # Recent Activity
    st.markdown("### 📝 Recent Activity")
    
    if ml_predictions:
        recent_preds = ml_predictions[-10:]
        recent_df = pd.DataFrame([
            {
                "Time": p.get('timestamp', 'N/A'),
                "Packets": p.get('packet_count', 0),
                "Threat": "🚨 Yes" if p.get('is_threat', False) else "✅ No",
                "Type": p.get('threat_type', 'Normal'),
                "Confidence": f"{p.get('confidence', 0):.1%}"
            }
            for p in recent_preds
        ])
        st.dataframe(recent_df, width="stretch", hide_index=True)
    else:
        st.info("No ML predictions yet. Start the analyzer to see real-time detections.")

# ==================== TAB 2: LIVE MONITORING ====================
with tab2:
    st.markdown("## 🔍 Live Network Monitoring")
    
    packets_df = load_packet_data()
    
    if not packets_df.empty:
        # Time filter
        time_range = st.selectbox(
            "Time Range",
            ["Last 5 minutes", "Last 15 minutes", "Last 1 hour", "Last 24 hours", "All time"]
        )
        
        # Filter data
        now = datetime.now()
        if time_range == "Last 5 minutes":
            filtered_df = packets_df[packets_df['Timestamp'] > now - timedelta(minutes=5)]
        elif time_range == "Last 15 minutes":
            filtered_df = packets_df[packets_df['Timestamp'] > now - timedelta(minutes=15)]
        elif time_range == "Last 1 hour":
            filtered_df = packets_df[packets_df['Timestamp'] > now - timedelta(hours=1)]
        elif time_range == "Last 24 hours":
            filtered_df = packets_df[packets_df['Timestamp'] > now - timedelta(hours=24)]
        else:
            filtered_df = packets_df
        
        # Metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Packets", len(filtered_df))
        with col2:
            # Handle both column name formats
            src_col = 'Src_IP' if 'Src_IP' in filtered_df.columns else 'Source IP'
            st.metric("Unique IPs", filtered_df[src_col].nunique() if src_col in filtered_df.columns else 0)
        with col3:
            st.metric("Protocols", filtered_df['Protocol'].nunique())
        with col4:
            size_col = 'Size' if 'Size' in filtered_df.columns else 'Packet Size'
            avg_size = filtered_df[size_col].mean() if size_col in filtered_df.columns else 0
            st.metric("Avg Size", f"{avg_size:.0f} bytes")
        
        st.markdown("---")
        
        # Visualizations
        col1, col2 = st.columns(2)
        
        with col1:
            # Top Source IPs
            src_col = 'Src_IP' if 'Src_IP' in filtered_df.columns else 'Source IP'
            if src_col in filtered_df.columns:
                top_ips = filtered_df[src_col].value_counts().head(10)
                fig = go.Figure(go.Bar(
                    x=top_ips.values,
                    y=top_ips.index,
                    orientation='h'
                ))
                fig.update_layout(
                    title="Top 10 Source IPs",
                    xaxis_title="Packet Count",
                    yaxis_title="IP Address"
                )
                st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
            else:
                st.info("Source IP data not available")
        
        with col2:
            # Protocol Distribution
            protocol_dist = filtered_df['Protocol'].value_counts()
            fig = px.pie(
                values=protocol_dist.values,
                names=protocol_dist.index,
                title="Protocol Distribution",
                hole=0.4
            )
            st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
        
        # Timeline
        st.markdown("### 📈 Traffic Timeline")
        if 'Timestamp' in filtered_df.columns:
            timeline = filtered_df.groupby(filtered_df['Timestamp'].dt.floor('1min')).size().reset_index()
            timeline.columns = ['Time', 'Packets']
            
            fig = px.line(
                timeline,
                x='Time',
                y='Packets',
                title="Packets per Minute"
            )
            st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
        
        # Raw Data
        with st.expander("📋 View Raw Packet Data"):
            st.dataframe(filtered_df.tail(100), width="stretch")
            
            # Export
            csv = filtered_df.to_csv(index=False)
            st.download_button(
                label="📥 Download as CSV",
                data=csv,
                file_name=f"packets_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    else:
        st.info("🔍 No packet data available. Start the analyzer or generate sample data to begin monitoring.")

# ==================== TAB 3: ML PREDICTIONS ====================
with tab3:
    st.markdown("## 🤖 Machine Learning Predictions")
    
    ml_predictions = load_ml_predictions()
    ml_stats = load_ml_stats()
    
    if ml_stats:
        # ML Statistics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Windows Processed", ml_stats.get('windows_processed', 0))
        with col2:
            st.metric("Total Packets", ml_stats.get('total_packets', 0))
        with col3:
            st.metric("Normal Traffic", ml_stats.get('normal_count', 0))
        with col4:
            st.metric("Threats Detected", ml_stats.get('threat_count', 0))
        
        st.markdown("---")
        
        # Packet Statistics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Mean Packet Size", f"{ml_stats.get('mean_packet_size', 0):.0f} bytes")
        with col2:
            st.metric("Max Packet Size", f"{ml_stats.get('max_packet_size', 0):.0f} bytes")
        with col3:
            st.metric("Min Packet Size", f"{ml_stats.get('min_packet_size', 0):.0f} bytes")
    
    if ml_predictions:
        st.markdown("### 📊 Prediction Analysis")
        
        # Create DataFrame
        pred_df = pd.DataFrame(ml_predictions)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Threat Distribution
            threat_counts = pred_df['is_threat'].value_counts()
            fig = px.pie(
                values=threat_counts.values,
                names=['Normal' if not x else 'Threat' for x in threat_counts.index],
                title="Threat vs Normal Traffic",
                color_discrete_sequence=['#00ff00', '#ff0000']
            )
            st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
        
        with col2:
            # Threat Types
            threat_types = pred_df[pred_df['is_threat'] == True]['threat_type'].value_counts()
            if not threat_types.empty:
                fig = go.Figure(go.Bar(
                    x=threat_types.index,
                    y=threat_types.values
                ))
                fig.update_layout(
                    title="Threat Types Detected",
                    xaxis_title="Threat Type",
                    yaxis_title="Count"
                )
                st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
            else:
                st.info("No threats detected yet")
        
        # Confidence Distribution
        st.markdown("### 📉 Confidence Scores")
        fig = px.histogram(
            pred_df,
            x='confidence',
            nbins=20,
            title="Prediction Confidence Distribution",
            labels={'confidence': 'Confidence Score'}
        )
        st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
        
        # Recent Predictions Table
        st.markdown("### 📝 Recent Predictions")
        recent_df = pred_df.tail(20).copy()
        recent_df['timestamp'] = pd.to_datetime(recent_df['timestamp'])
        recent_df['status'] = recent_df['is_threat'].apply(lambda x: '🚨 Threat' if x else '✅ Normal')
        recent_df['confidence_%'] = (recent_df['confidence'] * 100).round(2)
        
        display_df = recent_df[['timestamp', 'status', 'threat_type', 'confidence_%', 'packet_count']].sort_values('timestamp', ascending=False)
        st.dataframe(display_df, width="stretch", hide_index=True)
        
        # Export
        csv = pred_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Predictions as CSV",
            data=csv,
            file_name=f"ml_predictions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    else:
        st.info("🤖 No ML predictions available. Start the analyzer with a trained model to see real-time predictions.")
        
        if not check_model_exists():
            st.warning("⚠️ ML model not found. Train the model first using the sidebar.")

# ==================== TAB 4: THREAT ANALYSIS ====================
with tab4:
    st.markdown("## 🚨 Threat Analysis")
    
    threats = load_threat_data()
    
    if threats:
        threat_df = pd.DataFrame(threats)
        
        # All entries in threat logs are threats, no need to filter
        # Handle both formats: with 'threat' column or without
        if 'threat' in threat_df.columns:
            threat_only = threat_df[threat_df['threat'] == True]
        else:
            threat_only = threat_df  # All entries are threats
        
        if not threat_only.empty:
            # Threat Summary
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Threats", len(threat_only))
            with col2:
                # Check for 'type' or 'threat_type' column
                type_col = 'type' if 'type' in threat_only.columns else 'threat_type' if 'threat_type' in threat_only.columns else None
                unique_types = threat_only[type_col].nunique() if type_col else 0
                st.metric("Threat Types", unique_types)
            with col3:
                unique_ips = threat_only['source_ip'].nunique() if 'source_ip' in threat_only.columns else 0
                st.metric("Malicious IPs", unique_ips)
            with col4:
                if 'timestamp' in threat_only.columns:
                    threat_only['timestamp'] = pd.to_datetime(threat_only['timestamp'])
                    latest = threat_only['timestamp'].max()
                    time_since = datetime.now() - latest
                    st.metric("Last Threat", f"{time_since.seconds}s ago")
            
            st.markdown("---")
            
            # Visualizations
            col1, col2 = st.columns(2)
            
            with col1:
                # Threat Types
                type_counts = threat_only['threat_type'].value_counts()
                fig = go.Figure(go.Bar(
                    x=type_counts.index,
                    y=type_counts.values,
                    marker=dict(
                        color=type_counts.values,
                        colorscale='Reds'
                    )
                ))
                fig.update_layout(
                    title="Threats by Type",
                    xaxis_title="Threat Type",
                    yaxis_title="Count"
                )
                st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
            
            with col2:
                # Top Threat Sources
                if 'source_ip' in threat_only.columns:
                    top_sources = threat_only['source_ip'].value_counts().head(10)
                    fig = go.Figure(go.Bar(
                        x=top_sources.values,
                        y=top_sources.index,
                        orientation='h',
                        marker=dict(
                            color=top_sources.values,
                            colorscale='Reds'
                        )
                    ))
                    fig.update_layout(
                        title="Top 10 Threat Sources",
                        xaxis_title="Threat Count",
                        yaxis_title="IP Address"
                    )
                    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
            
            # Threat Timeline
            if 'timestamp' in threat_only.columns:
                st.markdown("### 📈 Threat Timeline")
                timeline = threat_only.groupby(threat_only['timestamp'].dt.floor('1min')).size().reset_index()
                timeline.columns = ['Time', 'Threats']
                
                fig = px.area(
                    timeline,
                    x='Time',
                    y='Threats',
                    title="Threats per Minute",
                    color_discrete_sequence=['#ff0000']
                )
                st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
            
            # Threat Details
            st.markdown("### 📋 Threat Details")
            st.dataframe(threat_only, width="stretch", hide_index=True)
            
            # Export
            csv = threat_only.to_csv(index=False)
            st.download_button(
                label="📥 Download Threat Report as CSV",
                data=csv,
                file_name=f"threat_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        else:
            st.success("✅ No threats detected! Your network is secure.")
    else:
        st.info("🔍 No threat data available. Start the analyzer to begin threat detection.")

# ==================== TAB 5: STATISTICS ====================
with tab5:
    st.markdown("## 📈 Network Statistics")
    
    packets_df = load_packet_data()
    threats = load_threat_data()
    ml_predictions = load_ml_predictions()
    
    if not packets_df.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 Packet Statistics")
            
            size_col = 'Size' if 'Size' in packets_df.columns else 'Packet Size'
            if size_col in packets_df.columns:
                size_stats = packets_df[size_col].describe()
                stats_df = pd.DataFrame({
                    'Metric': ['Count', 'Mean', 'Std Dev', 'Min', '25%', '50%', '75%', 'Max'],
                    'Value': [
                        f"{size_stats['count']:.0f}",
                        f"{size_stats['mean']:.2f} bytes",
                        f"{size_stats['std']:.2f} bytes",  # Fixed: added " bytes"
                        f"{size_stats['min']:.0f} bytes",
                        f"{size_stats['25%']:.0f} bytes",
                        f"{size_stats['50%']:.0f} bytes",
                        f"{size_stats['75%']:.0f} bytes",
                        f"{size_stats['max']:.0f} bytes"
                    ]
                })
                st.dataframe(stats_df, width="stretch", hide_index=True)
            else:
                st.info("Packet size data not available")
        
        with col2:
            st.markdown("### 🌐 Network Overview")
            
            src_col = 'Src_IP' if 'Src_IP' in packets_df.columns else 'Source IP'
            dst_col = 'Dst_IP' if 'Dst_IP' in packets_df.columns else 'Destination IP'
            
            network_stats = {
                'Metric': [
                    'Total Packets',
                    'Unique Source IPs',
                    'Unique Dest IPs',
                    'Protocols',
                    'Time Span'
                ],
                'Value': [
                    f"{len(packets_df):,}",
                    f"{packets_df[src_col].nunique()}" if src_col in packets_df.columns else "0",
                    f"{packets_df[dst_col].nunique()}" if dst_col in packets_df.columns else "0",
                    f"{packets_df['Protocol'].nunique()}",
                    f"{(packets_df['Timestamp'].max() - packets_df['Timestamp'].min()).total_seconds():.0f}s"
                    if 'Timestamp' in packets_df.columns else 'N/A'
                ]
            }
            st.dataframe(pd.DataFrame(network_stats), width="stretch", hide_index=True)
        
        # Protocol Analysis
        st.markdown("### 📡 Protocol Analysis")
        size_col = 'Size' if 'Size' in packets_df.columns else 'Packet Size'
        if size_col in packets_df.columns:
            protocol_stats = packets_df.groupby('Protocol').agg({
                size_col: ['count', 'mean', 'sum']
            }).round(2)
            protocol_stats.columns = ['Count', 'Avg Size', 'Total Bytes']
        else:
            protocol_stats = packets_df.groupby('Protocol').size().to_frame('Count')
        st.dataframe(protocol_stats, width="stretch")
        
        # IP Analysis
        st.markdown("### 🌐 Top IP Addresses")
        col1, col2 = st.columns(2)
        
        src_col = 'Src_IP' if 'Src_IP' in packets_df.columns else 'Source IP'
        dst_col = 'Dst_IP' if 'Dst_IP' in packets_df.columns else 'Destination IP'
        
        with col1:
            st.markdown("**Top Source IPs**")
            if src_col in packets_df.columns:
                top_src = packets_df[src_col].value_counts().head(10)
                st.dataframe(
                    pd.DataFrame({'IP': top_src.index, 'Packets': top_src.values}),
                    width="stretch",
                    hide_index=True
                )
            else:
                st.info("Source IP data not available")
        
        with col2:
            st.markdown("**Top Destination IPs**")
            if dst_col in packets_df.columns:
                top_dst = packets_df[dst_col].value_counts().head(10)
                st.dataframe(
                    pd.DataFrame({'IP': top_dst.index, 'Packets': top_dst.values}),
                    width="stretch",
                    hide_index=True
                )
            else:
                st.info("Destination IP data not available")
    else:
        st.info("📊 No data available for statistics. Generate sample data or start the analyzer.")

# ==================== TAB 6: FEATURES & GUIDE ====================
with tab6:
    st.markdown("## ℹ️ NetGuard AI - Features & User Guide")
    
    st.markdown("""
    <div class='success-box'>
        <h3>🎉 Welcome to NetGuard AI!</h3>
        <p>Your complete network security monitoring and threat detection platform with ML capabilities.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🚀 What You Can Do")
    
    features = [
        {
            "Feature": "🤖 Train ML Model",
            "Description": "Train a Random Forest classifier with 27+ features for threat detection",
            "Location": "Sidebar → ML Model Training",
            "Action": "Click 'Train ML Model' button"
        },
        {
            "Feature": "▶️ Start/Stop Analyzer",
            "Description": "Control real-time packet capture and analysis",
            "Location": "Sidebar → Real-Time Analyzer",
            "Action": "Click Start/Stop buttons"
        },
        {
            "Feature": "📊 Generate Sample Data",
            "Description": "Create test data for exploring dashboard features",
            "Location": "Sidebar → Test Data",
            "Action": "Click 'Generate Sample Data'"
        },
        {
            "Feature": "🔍 Live Monitoring",
            "Description": "Real-time packet capture visualization with protocol analysis",
            "Location": "Live Monitoring Tab",
            "Action": "View traffic patterns and filter by time"
        },
        {
            "Feature": "🤖 ML Predictions",
            "Description": "View ML model predictions with confidence scores",
            "Location": "ML Predictions Tab",
            "Action": "Analyze threat classifications"
        },
        {
            "Feature": "🚨 Threat Analysis",
            "Description": "Detailed threat detection and analysis",
            "Location": "Threat Analysis Tab",
            "Action": "View threat types and sources"
        },
        {
            "Feature": "📈 Statistics",
            "Description": "Comprehensive network statistics and metrics",
            "Location": "Statistics Tab",
            "Action": "Explore detailed analytics"
        },
        {
            "Feature": "📥 Export Data",
            "Description": "Download data as CSV for further analysis",
            "Location": "Available in each tab",
            "Action": "Click download buttons"
        },
        {
            "Feature": "🔄 Auto-Refresh",
            "Description": "Automatic dashboard updates for live monitoring",
            "Location": "Sidebar → Auto-Refresh",
            "Action": "Enable/disable and set interval"
        }
    ]
    
    st.dataframe(pd.DataFrame(features), width="stretch", hide_index=True)
    
    st.markdown("---")
    
    st.markdown("### 📝 Step-by-Step Guide")
    
    st.markdown("""
    <div class='info-box'>
        <h4>🎯 Getting Started (First Time)</h4>
        <ol>
            <li><strong>Train the ML Model:</strong> Click "Train ML Model" in the sidebar (takes ~30 seconds)</li>
            <li><strong>Generate Sample Data:</strong> Click "Generate Sample Data" to create test traffic</li>
            <li><strong>Explore Tabs:</strong> Navigate through all tabs to see the features</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class='info-box'>
        <h4>🔍 Real-Time Monitoring</h4>
        <ol>
            <li><strong>Start Analyzer:</strong> Click "Start" in Real-Time Analyzer section (requires sudo)</li>
            <li><strong>Enable Auto-Refresh:</strong> Check "Enable Auto-Refresh" and set interval (1-10s)</li>
            <li><strong>Watch Live Data:</strong> Go to "Live Monitoring" tab to see real-time capture</li>
            <li><strong>Monitor Threats:</strong> Check "Threat Analysis" tab for any detections</li>
            <li><strong>View ML Predictions:</strong> See ML model's classifications in "ML Predictions" tab</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class='warning-box'>
        <h4>⚠️ Important Notes</h4>
        <ul>
            <li><strong>Sudo Access:</strong> Real-time analyzer requires sudo/root for packet capture</li>
            <li><strong>Network Interface:</strong> Analyzer will use default network interface</li>
            <li><strong>Performance:</strong> Auto-refresh with short intervals may use more CPU</li>
            <li><strong>Data Limits:</strong> System stores last 10,000 packets to prevent memory issues</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### 🎨 Dashboard Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### 📊 Visualizations Available
        - Protocol distribution (pie charts)
        - Top source/destination IPs (bar charts)
        - Traffic timeline (line/area charts)
        - Threat type analysis (bar charts)
        - Packet size distribution (histograms)
        - Confidence score distribution (histograms)
        """)
    
    with col2:
        st.markdown("""
        #### 📥 Export Options
        - Raw packet data (CSV)
        - ML predictions (CSV)
        - Threat reports (CSV)
        - Custom time-filtered data
        - Complete dataset export
        """)
    
    st.markdown("---")
    
    st.markdown("### 🤖 ML Features")
    
    st.markdown("""
    <div class='info-box'>
        <h4>🧠 27+ Features Analyzed</h4>
        <ul>
            <li><strong>Packet Statistics:</strong> Count, unique IPs, unique ports</li>
            <li><strong>Byte Statistics:</strong> Total, mean, max, min, std deviation</li>
            <li><strong>Protocol Distribution:</strong> TCP, UDP, ICMP counts</li>
            <li><strong>Port Analysis:</strong> HTTP, HTTPS, DNS, SSH traffic</li>
            <li><strong>TTL Features:</strong> Mean, min, max TTL values</li>
            <li><strong>Time Features:</strong> Duration, packets per second</li>
            <li><strong>Entropy Measures:</strong> Source/destination IP entropy</li>
            <li><strong>Flow Patterns:</strong> Max IP counts, distribution metrics</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### 🎯 Use Cases")
    
    use_cases = [
        {
            "Use Case": "🔍 Network Monitoring",
            "Description": "Track all network traffic in real-time",
            "How": "Start analyzer + Enable auto-refresh + Monitor Live tab"
        },
        {
            "Use Case": "🚨 Threat Detection",
            "Description": "Identify suspicious network activity",
            "How": "Train model + Start analyzer + Check Threat Analysis tab"
        },
        {
            "Use Case": "📊 Traffic Analysis",
            "Description": "Understand network patterns and usage",
            "How": "Capture traffic + View Statistics tab + Export data"
        },
        {
            "Use Case": "🤖 ML Training",
            "Description": "Train custom threat detection models",
            "How": "Generate/collect data + Train model + Validate predictions"
        },
        {
            "Use Case": "📈 Security Auditing",
            "Description": "Generate security reports and logs",
            "How": "Run analyzer over time + Export threat reports + Analyze patterns"
        }
    ]
    
    st.dataframe(pd.DataFrame(use_cases), width="stretch", hide_index=True)
    
    st.markdown("---")
    
    st.markdown("""
    <div class='success-box'>
        <h3>🎉 You're All Set!</h3>
        <p>Start exploring NetGuard AI's features. Begin with the Overview tab to see your system status,
        then train the ML model and start the analyzer for real-time monitoring!</p>
    </div>
    """, unsafe_allow_html=True)

# Auto-refresh logic
if auto_refresh:
    time_since_refresh = (datetime.now() - st.session_state.last_refresh).total_seconds()
    if time_since_refresh >= refresh_interval:
        st.session_state.last_refresh = datetime.now()
        time.sleep(0.1)
        st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p>🛡️ NetGuard AI - Network Security Monitoring Platform</p>
    <p>Real-Time Threat Detection • ML-Powered Analysis • Comprehensive Monitoring</p>
</div>
""", unsafe_allow_html=True)
