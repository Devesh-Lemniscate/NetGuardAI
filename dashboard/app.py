import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import os
from datetime import datetime, timedelta
import time

st.set_page_config(
    page_title="🛡️ NetGuard AI Dashboard", 
    page_icon="🛡️", 
    layout="wide"
)

st.title("🛡️ NetGuard AI - Network Threat Detection Dashboard")
st.markdown("---")

# File paths
PACKETS_LOG = "../data/packets_log.csv"
THREATS_LOG = "../data/threat_logs.json"

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
                    df['timestamp'] = pd.to_datetime(df['timestamp'])
                    return df
        except Exception as e:
            st.error(f"Error loading threat data: {e}")
    return pd.DataFrame()

# Main dashboard
col1, col2, col3 = st.columns(3)

# Load data
packet_df = load_packet_data()
threat_df = load_threat_data()

with col1:
    st.metric(
        label="📦 Total Packets Captured",
        value=len(packet_df) if not packet_df.empty else 0
    )

with col2:
    st.metric(
        label="🚨 Threats Detected",
        value=len(threat_df) if not threat_df.empty else 0
    )

with col3:
    recent_threats = len(threat_df[threat_df['timestamp'] > (datetime.now() - timedelta(hours=1))]) if not threat_df.empty else 0
    st.metric(
        label="⚡ Recent Threats (1h)",
        value=recent_threats
    )

st.markdown("---")

# Charts
if not packet_df.empty:
    st.subheader("📊 Network Traffic Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Protocol distribution
        protocol_counts = packet_df['Protocol'].value_counts()
        fig_pie = px.pie(
            values=protocol_counts.values,
            names=protocol_counts.index,
            title="Protocol Distribution"
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # Top source IPs
        top_ips = packet_df['Src_IP'].value_counts().head(10)
        fig_bar = px.bar(
            x=top_ips.values,
            y=top_ips.index,
            orientation='h',
            title="Top Source IPs",
            labels={'x': 'Packet Count', 'y': 'Source IP'}
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    # Traffic over time
    if len(packet_df) > 1:
        st.subheader("📈 Traffic Over Time")
        packet_df['hour'] = packet_df['Timestamp'].dt.floor('H')
        hourly_traffic = packet_df.groupby('hour').size().reset_index(name='count')
        
        fig_line = px.line(
            hourly_traffic,
            x='hour',
            y='count',
            title="Packets per Hour",
            labels={'hour': 'Time', 'count': 'Packet Count'}
        )
        st.plotly_chart(fig_line, use_container_width=True)

else:
    st.info("📡 No packet data available yet. Start the packet capture to see network traffic.")

# Threat Analysis
if not threat_df.empty:
    st.markdown("---")
    st.subheader("🚨 Threat Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Threat types
        threat_types = threat_df['threat_type'].value_counts()
        fig_threats = px.bar(
            x=threat_types.index,
            y=threat_types.values,
            title="Threat Types Detected",
            labels={'x': 'Threat Type', 'y': 'Count'}
        )
        st.plotly_chart(fig_threats, use_container_width=True)
    
    with col2:
        # Recent threats table
        st.subheader("Recent Threats")
        recent_threats = threat_df.sort_values('timestamp', ascending=False).head(10)
        st.dataframe(
            recent_threats[['timestamp', 'threat_type', 'source_ip', 'severity']],
            use_container_width=True
        )

else:
    st.info("🛡️ No threats detected yet. The system is monitoring for suspicious activity.")

# Auto-refresh
st.markdown("---")
if st.button("🔄 Refresh Dashboard"):
    st.rerun()

st.markdown("---")
st.markdown("*Dashboard last updated: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "*")
