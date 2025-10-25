#!/usr/bin/env python3
"""Generate sample data for NetGuard AI dashboard testing"""

import pandas as pd
import json
from datetime import datetime, timedelta
import random
import os

def generate_sample_data():
    print('📊 Generating sample data for dashboard...')
    
    # Ensure data directory exists
    os.makedirs('data', exist_ok=True)
    
    # Generate sample packet data
    timestamps = [datetime.now() - timedelta(minutes=i) for i in range(100, 0, -1)]
    src_ips = ['192.168.1.100', '192.168.1.101', '10.0.0.5', '172.16.0.10', '8.8.8.8']
    dst_ips = ['8.8.8.8', '1.1.1.1', '192.168.1.1', '172.217.0.0', '74.125.224.72']
    protocols = [6, 17, 1]  # TCP, UDP, ICMP
    ports = [80, 443, 53, 22, 3389, 8080]
    
    packet_data = []
    for ts in timestamps:
        packet_data.append({
            'Timestamp': ts,
            'Src_IP': random.choice(src_ips),
            'Dst_IP': random.choice(dst_ips), 
            'Protocol': random.choice(protocols),
            'Src_Port': random.randint(30000, 65000),
            'Dst_Port': random.choice(ports),
            'Size': random.randint(64, 1500)
        })
    
    # Save packet data
    df = pd.DataFrame(packet_data)
    df.to_csv('data/packets_log.csv', index=False)
    print(f'✅ Created {len(df)} sample packets in data/packets_log.csv')
    
    # Generate sample threat data
    threat_data = []
    threat_types = ['Port Scan', 'DDoS Attack', 'Suspicious Traffic', 'Brute Force']
    severities = ['Low', 'Medium', 'High', 'Critical']
    
    for i in range(20):
        threat_data.append({
            'timestamp': (datetime.now() - timedelta(minutes=random.randint(1, 120))).isoformat(),
            'threat_type': random.choice(threat_types),
            'source_ip': random.choice(src_ips[:3]),
            'severity': random.choice(severities),
            'description': 'Detected suspicious activity from source'
        })
    
    # Save threat data
    with open('data/threat_logs.json', 'w') as f:
        json.dump(threat_data, f, indent=2)
    
    print(f'✅ Created {len(threat_data)} sample threats in data/threat_logs.json')
    print('✅ Sample data generation complete!')

if __name__ == '__main__':
    generate_sample_data()
