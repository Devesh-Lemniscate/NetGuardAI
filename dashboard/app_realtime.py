"""
Real-Time Dashboard for NetGuard AI with ML Integration
Shows live packet capture, ML predictions, and threat alerts
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import os
from datetime import datetime, timedelta
import time
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="🛡️ NetGuard AI - Real-Time Dashboard", 
    page_icon="🛡️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for animations and styling
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
    
    .metric-card {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 8px;
        margin: 5px 0;
    }
    
    .stMetric {
        background-color: #ffffff;
        padding: 10px;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# File paths
PACKETS_LOG = "../data/packets_log.csv"
THREATS_LOG = "../data/threat_logs.json"
ML_PREDICTIONS_LOG = "../data/ml_predictions.json"
ML_STATS_LOG = "../data/ml_stats.json"

# Session state for alerts
if 'last_threat_time' not in st.session_state:
    st.session_state.last_threat_time = None
if 'threat_count' not in st.session_state:
    st.session_state.threat_count = 0

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
                threats = json.load(f)
                if threats:
                    df = pd.DataFrame(threats)
                    if 'timestamp' in df.columns:
                        df['timestamp'] = pd.to_datetime(df['timestamp'])
                    return df
        except Exception as e:
            pass
    return pd.DataFrame()

def load_ml_predictions():
    """Load ML prediction data"""
    if os.path.exists(ML_PREDICTIONS_LOG):
        try:
            with open(ML_PREDICTIONS_LOG, 'r') as f:
                predictions = json.load(f)
                if predictions:
                    df = pd.DataFrame(predictions)
                    df['timestamp'] = pd.to_datetime(df['timestamp'])
                    return df
        except Exception as e:
            pass
    return pd.DataFrame()

def load_ml_stats():
    """Load ML analyzer statistics"""
    if os.path.exists(ML_STATS_LOG):
        try:
            with open(ML_STATS_LOG, 'r') as f:
                return json.load(f)
        except Exception as e:
            pass
    return {}

def export_logs():
    """Export all logs to CSV"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Export packets
    packet_df = load_packet_data()
    if not packet_df.empty:
        packet_file = f"../data/export_packets_{timestamp}.csv"
        packet_df.to_csv(packet_file, index=False)
    
    # Export threats
    threat_df = load_threat_data()
    if not threat_df.empty:
        threat_file = f"../data/export_threats_{timestamp}.csv"
        threat_df.to_csv(threat_file, index=False)
    
    # Export ML predictions
    ml_df = load_ml_predictions()
    if not ml_df.empty:
        ml_file = f"../data/export_ml_predictions_{timestamp}.csv"
        ml_df.to_csv(ml_file, index=False)
        return timestamp
    
    return timestamp

# Sidebar
with st.sidebar:
    st.header("⚙️ Dashboard Controls")
    
    # Auto-refresh toggle
    auto_refresh = st.checkbox("🔄 Auto-refresh", value=True)
    
    if auto_refresh:
        refresh_rate = st.slider("Refresh rate (seconds)", 1, 10, 2)
    
    st.markdown("---")
    
    # Time filter
    st.subheader("📅 Time Filter")
    time_filter = st.selectbox(
        "Show data from",
        ["Last 5 minutes", "Last 15 minutes", "Last hour", "Last 24 hours", "All time"]
    )
    
    st.markdown("---")
    
    # Export button
    if st.button("📥 Export All Logs"):
        timestamp = export_logs()
        st.success(f"✅ Logs exported! Check data/ folder")
    
    st.markdown("---")
    
    # System info
    st.subheader("📊 System Info")
    ml_stats = load_ml_stats()
    if ml_stats:
        st.metric("Analyzer Status", "🟢 Running" if ml_stats.get('running', False) else "🔴 Stopped")
        st.metric("Window Size", f"{ml_stats.get('window_size', 5)}s")
        st.metric("Buffer Size", ml_stats.get('buffer_size', 0))

# Main dashboard title
st.title("🛡️ NetGuard AI - Real-Time Dashboard")
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
st.caption(f"Last updated: {current_time}")

# Load all data
packet_df = load_packet_data()
threat_df = load_threat_data()
ml_df = load_ml_predictions()
ml_stats = load_ml_stats()

# Apply time filter
def apply_time_filter(df, time_col='Timestamp'):
    if df.empty or time_filter == "All time":
        return df
    
    now = datetime.now()
    if time_filter == "Last 5 minutes":
        cutoff = now - timedelta(minutes=5)
    elif time_filter == "Last 15 minutes":
        cutoff = now - timedelta(minutes=15)
    elif time_filter == "Last hour":
        cutoff = now - timedelta(hours=1)
    elif time_filter == "Last 24 hours":
        cutoff = now - timedelta(hours=24)
    else:
        return df
    
    if time_col in df.columns:
        return df[df[time_col] >= cutoff]
    return df

packet_df = apply_time_filter(packet_df, 'Timestamp')
threat_df = apply_time_filter(threat_df, 'timestamp')
ml_df = apply_time_filter(ml_df, 'timestamp')

# Check for recent threats
recent_threats = ml_df[ml_df['is_threat'] == True] if not ml_df.empty and 'is_threat' in ml_df.columns else pd.DataFrame()
if not recent_threats.empty:
    latest_threat = recent_threats.iloc[-1]
    if st.session_state.last_threat_time != latest_threat['timestamp']:
        st.session_state.last_threat_time = latest_threat['timestamp']
        st.session_state.threat_count += 1

# Threat Alert Banner
if not recent_threats.empty and len(recent_threats) > 0:
    latest_threat = recent_threats.iloc[-1]
    time_since = (datetime.now() - latest_threat['timestamp']).total_seconds()
    
    if time_since < 30:  # Show alert for threats in last 30 seconds
        st.markdown(f"""
        <div class="threat-alert">
            🚨 THREAT DETECTED! 🚨<br>
            Type: {latest_threat.get('threat_type', 'Unknown')}<br>
            Confidence: {latest_threat.get('confidence', 0)*100:.1f}%<br>
            {int(time_since)}s ago
        </div>
        """, unsafe_allow_html=True)
        
        # Play sound/notification (browser will handle this)
        st.toast(f"⚠️ Threat detected: {latest_threat.get('threat_type', 'Unknown')}", icon="🚨")
else:
    st.markdown("""
    <div class="normal-status">
        ✅ SYSTEM SECURE - No Recent Threats
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Top metrics row
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    total_packets = len(packet_df) if not packet_df.empty else 0
    st.metric(
        label="📦 Total Packets",
        value=f"{total_packets:,}",
        delta=f"+{ml_stats.get('total_packets', 0) - total_packets}" if ml_stats else None
    )

with col2:
    windows_processed = ml_stats.get('total_predictions', 0)
    st.metric(
        label="🔍 Windows Processed",
        value=windows_processed
    )

with col3:
    if not packet_df.empty and 'Size' in packet_df.columns:
        mean_size = int(packet_df['Size'].mean())
        st.metric(
            label="📊 Mean Packet Size",
            value=f"{mean_size} bytes"
        )
    else:
        st.metric(label="📊 Mean Packet Size", value="N/A")

with col4:
    normal_count = len(ml_df[ml_df['is_threat'] == False]) if not ml_df.empty and 'is_threat' in ml_df.columns else 0
    st.metric(
        label="✅ Normal Windows",
        value=normal_count
    )

with col5:
    threat_count = len(ml_df[ml_df['is_threat'] == True]) if not ml_df.empty and 'is_threat' in ml_df.columns else 0
    st.metric(
        label="🚨 Threat Windows",
        value=threat_count,
        delta=f"{threat_count} detected"
    )

st.markdown("---")

# Packet Statistics Row
if not packet_df.empty and 'Size' in packet_df.columns:
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📏 Min Packet Size", f"{int(packet_df['Size'].min())} bytes")
    with col2:
        st.metric("📏 Max Packet Size", f"{int(packet_df['Size'].max())} bytes")
    with col3:
        st.metric("📏 Std Packet Size", f"{int(packet_df['Size'].std())} bytes")
    with col4:
        st.metric("📊 Total Bytes", f"{int(packet_df['Size'].sum()):,} bytes")
    
    st.markdown("---")

# Charts Section
tab1, tab2, tab3, tab4 = st.tabs(["📊 Traffic Analysis", "🤖 ML Predictions", "🚨 Threat Details", "📈 Time Series"])

with tab1:
    if not packet_df.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            # Protocol distribution
            st.subheader("Protocol Distribution")
            if 'Protocol' in packet_df.columns:
                protocol_map = {6: 'TCP', 17: 'UDP', 1: 'ICMP'}
                packet_df['Protocol_Name'] = packet_df['Protocol'].map(protocol_map).fillna('Other')
                protocol_counts = packet_df['Protocol_Name'].value_counts()
                
                fig = px.pie(
                    values=protocol_counts.values,
                    names=protocol_counts.index,
                    title="Traffic by Protocol",
                    color_discrete_sequence=px.colors.sequential.RdBu
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Top source IPs
            st.subheader("Top Source IPs")
            if 'Src_IP' in packet_df.columns:
                top_ips = packet_df['Src_IP'].value_counts().head(10)
                fig = px.bar(
                    x=top_ips.values,
                    y=top_ips.index,
                    orientation='h',
                    title="Most Active Source IPs",
                    labels={'x': 'Packet Count', 'y': 'Source IP'},
                    color=top_ips.values,
                    color_continuous_scale='Reds'
                )
                st.plotly_chart(fig, use_container_width=True)
        
        # Packet size distribution
        st.subheader("Packet Size Distribution")
        if 'Size' in packet_df.columns:
            fig = px.histogram(
                packet_df,
                x='Size',
                nbins=50,
                title="Distribution of Packet Sizes",
                labels={'Size': 'Packet Size (bytes)', 'count': 'Frequency'},
                color_discrete_sequence=['#1f77b4']
            )
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("📡 No packet data available yet. Start packet capture to see traffic analysis.")

with tab2:
    st.subheader("🤖 ML Prediction Results")
    
    if not ml_df.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            # Threat vs Normal
            if 'is_threat' in ml_df.columns:
                threat_counts = ml_df['is_threat'].value_counts()
                threat_labels = ['Normal' if not x else 'Threat' for x in threat_counts.index]
                
                fig = go.Figure(data=[go.Pie(
                    labels=threat_labels,
                    values=threat_counts.values,
                    marker=dict(colors=['#00ff00', '#ff0000']),
                    hole=0.4
                )])
                fig.update_layout(title="Normal vs Threat Classification")
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Threat types
            if 'threat_type' in ml_df.columns:
                threat_types = ml_df[ml_df['is_threat'] == True]['threat_type'].value_counts()
                if len(threat_types) > 0:
                    fig = px.bar(
                        x=threat_types.index,
                        y=threat_types.values,
                        title="Threat Types Detected",
                        labels={'x': 'Threat Type', 'y': 'Count'},
                        color=threat_types.values,
                        color_continuous_scale='Reds'
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("✅ No threats detected!")
        
        # Confidence distribution
        st.subheader("Prediction Confidence Distribution")
        if 'confidence' in ml_df.columns:
            fig = px.histogram(
                ml_df,
                x='confidence',
                nbins=20,
                title="Distribution of Prediction Confidence Scores",
                labels={'confidence': 'Confidence', 'count': 'Frequency'},
                color_discrete_sequence=['#9467bd']
            )
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("🤖 No ML predictions yet. Run the ML analyzer to see predictions.")

with tab3:
    st.subheader("🚨 Threat Log")
    
    threat_display_df = ml_df[ml_df['is_threat'] == True] if not ml_df.empty and 'is_threat' in ml_df.columns else pd.DataFrame()
    
    if not threat_display_df.empty:
        # Display as table
        display_cols = ['timestamp', 'threat_type', 'confidence']
        if all(col in threat_display_df.columns for col in display_cols):
            threat_table = threat_display_df[display_cols].copy()
            threat_table['confidence'] = threat_table['confidence'].apply(lambda x: f"{x*100:.1f}%")
            threat_table = threat_table.sort_values('timestamp', ascending=False)
            
            st.dataframe(
                threat_table,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "timestamp": st.column_config.DatetimeColumn("Time", format="DD/MM/YY HH:mm:ss"),
                    "threat_type": "Threat Type",
                    "confidence": "Confidence"
                }
            )
            
            # Recent threat details
            st.subheader("Latest Threat Details")
            latest = threat_display_df.iloc[-1]
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("🕒 Time", latest['timestamp'].strftime("%H:%M:%S"))
            with col2:
                st.metric("⚠️ Type", latest['threat_type'])
            with col3:
                st.metric("🎯 Confidence", f"{latest['confidence']*100:.1f}%")
            
            # Feature details if available
            if 'features' in latest and isinstance(latest['features'], dict):
                st.subheader("Feature Values")
                features = latest['features']
                
                col1, col2, col3, col4 = st.columns(4)
                feature_items = list(features.items())
                
                for i, (key, value) in enumerate(feature_items[:12]):
                    col = [col1, col2, col3, col4][i % 4]
                    with col:
                        st.metric(key.replace('_', ' ').title(), f"{value:.2f}" if isinstance(value, float) else value)
    else:
        st.success("✅ No threats detected! System is secure.")

with tab4:
    st.subheader("📈 Time Series Analysis")
    
    if not packet_df.empty and 'Timestamp' in packet_df.columns:
        # Packets over time
        packet_df['minute'] = packet_df['Timestamp'].dt.floor('T')
        packets_per_minute = packet_df.groupby('minute').size().reset_index(name='count')
        
        fig = px.line(
            packets_per_minute,
            x='minute',
            y='count',
            title="Packets per Minute",
            labels={'minute': 'Time', 'count': 'Packet Count'},
            markers=True
        )
        fig.update_traces(line_color='#1f77b4', line_width=2)
        st.plotly_chart(fig, use_container_width=True)
        
        # Bytes over time
        if 'Size' in packet_df.columns:
            bytes_per_minute = packet_df.groupby('minute')['Size'].sum().reset_index(name='bytes')
            
            fig = px.area(
                bytes_per_minute,
                x='minute',
                y='bytes',
                title="Bytes Transferred per Minute",
                labels={'minute': 'Time', 'bytes': 'Bytes'},
                color_discrete_sequence=['#ff7f0e']
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # ML predictions over time
    if not ml_df.empty and 'timestamp' in ml_df.columns:
        ml_df['minute'] = ml_df['timestamp'].dt.floor('T')
        threats_per_minute = ml_df.groupby(['minute', 'is_threat']).size().reset_index(name='count')
        
        fig = px.bar(
            threats_per_minute,
            x='minute',
            y='count',
            color='is_threat',
            title="Predictions per Minute (Normal vs Threat)",
            labels={'minute': 'Time', 'count': 'Count', 'is_threat': 'Is Threat'},
            color_discrete_map={True: '#ff0000', False: '#00ff00'}
        )
        st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.caption(f"🕒 Dashboard started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
with col2:
    st.caption(f"📊 Data source: Live analysis")
with col3:
    st.caption(f"🔄 Auto-refresh: {'Enabled' if auto_refresh else 'Disabled'}")

# Auto-refresh
if auto_refresh:
    time.sleep(refresh_rate)
    st.rerun()
