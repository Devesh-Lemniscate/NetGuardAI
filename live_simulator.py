#!/usr/bin/env python3
"""
Simple live data simulator - generates realistic network traffic without needing sudo
"""

import time
import json
import random
import os
from datetime import datetime
from pathlib import Path

# Get base directory
base_dir = Path(__file__).parent
ml_pred_file = base_dir / 'data' / 'ml_predictions.json'
ml_stats_file = base_dir / 'data' / 'ml_stats.json'
packets_file = base_dir / 'data' / 'packets_log.csv'

# Sample IPs
IPS = ['192.168.1.100', '192.168.1.101', '192.168.1.102', '8.8.8.8', '1.1.1.1', 
       '104.244.42.129', '151.101.1.140', '142.250.185.206']

# Protocols
PROTOCOLS = ['TCP', 'UDP', 'ICMP']

# Threat types
THREAT_TYPES = ['normal', 'port_scan', 'ddos_attack', 'malware_detected', 'data_exfiltration']

def generate_live_packet():
    """Generate a realistic packet"""
    return {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'src_ip': random.choice(IPS),
        'dst_ip': random.choice(IPS),
        'protocol': random.choice(PROTOCOLS),
        'src_port': random.randint(1024, 65535),
        'dst_port': random.choice([80, 443, 22, 3389, 8080]),
        'size': random.randint(64, 1500)
    }

def generate_prediction():
    """Generate ML prediction"""
    is_threat = random.random() < 0.15  # 15% chance of threat
    
    if is_threat:
        threat_type = random.choice(THREAT_TYPES[1:])  # Exclude 'normal'
        confidence = random.uniform(0.7, 0.95)
    else:
        threat_type = 'normal'
        confidence = random.uniform(0.6, 0.9)
    
    return {
        'timestamp': datetime.now().isoformat(),
        'is_threat': is_threat,
        'threat_type': threat_type,
        'confidence': confidence,
        'features': {
            'total_packets': random.randint(50, 500),
            'unique_src_ips': random.randint(5, 30),
            'unique_dst_ips': random.randint(5, 30),
            'total_bytes': random.randint(10000, 100000)
        }
    }

def main():
    """Main loop - generates live data"""
    print("🚀 Live data simulator started")
    print("📊 Generating packets every 2 seconds...")
    print("Press Ctrl+C to stop")
    
    # Ensure data directory exists
    os.makedirs(base_dir / 'data', exist_ok=True)
    
    predictions = []
    total_packets = 0
    
    try:
        while True:
            # Generate 5-10 packets
            num_packets = random.randint(5, 10)
            
            # Append to CSV (simulating live capture)
            with open(packets_file, 'a') as f:
                for _ in range(num_packets):
                    pkt = generate_live_packet()
                    line = f"{pkt['timestamp']},{pkt['src_ip']},{pkt['dst_ip']},{pkt['protocol']},{pkt['src_port']},{pkt['dst_port']},{pkt['size']}\n"
                    f.write(line)
                    total_packets += 1
            
            # Generate prediction
            pred = generate_prediction()
            predictions.append(pred)
            
            # Keep only last 100 predictions
            if len(predictions) > 100:
                predictions = predictions[-100:]
            
            # Save predictions
            with open(ml_pred_file, 'w') as f:
                json.dump(predictions, f, indent=2)
            
            # Save stats
            stats = {
                'total_packets': total_packets,
                'total_predictions': len(predictions),
                'threats_detected': sum(1 for p in predictions if p['is_threat'])
            }
            
            with open(ml_stats_file, 'w') as f:
                json.dump(stats, f, indent=2)
            
            print(f"📊 Packets: {total_packets}, Predictions: {len(predictions)}, Threats: {stats['threats_detected']}")
            
            time.sleep(2)
    
    except KeyboardInterrupt:
        print("\n✅ Stopped")

if __name__ == '__main__':
    main()
