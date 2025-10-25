#!/bin/bash

echo "🧪 TESTING PACKET CAPTURE"
echo "========================"
echo ""

echo "1️⃣ Testing basic packet capture with tcpdump..."
echo "   (This will capture 5 packets from wlo1 interface)"
echo ""

sudo timeout 5 tcpdump -i wlo1 -c 5 2>&1 | head -10

echo ""
echo "2️⃣ Testing Python/Scapy packet capture..."
echo "   (Running simple test script)"
echo ""

sudo .venv/bin/python3 << 'EOF'
from scapy.all import sniff
import sys

print("Attempting to capture 3 packets from wlo1...")
try:
    packets = sniff(iface="wlo1", count=3, timeout=5)
    print(f"✅ Successfully captured {len(packets)} packets!")
    for i, pkt in enumerate(packets, 1):
        print(f"   Packet {i}: {pkt.summary()}")
    sys.exit(0)
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)
EOF

RESULT=$?

echo ""
echo "========================"
if [ $RESULT -eq 0 ]; then
    echo "✅ Scapy CAN capture packets!"
    echo ""
    echo "💡 The issue is likely in the realtime_analyzer.py code."
    echo "   Let's check the analyzer output for errors..."
else
    echo "❌ Scapy CANNOT capture packets!"
    echo ""
    echo "💡 SOLUTIONS:"
    echo "   1. Install required packages: sudo apt-get install libpcap-dev"
    echo "   2. Check permissions: Make sure you're using sudo"
    echo "   3. Try: sudo setcap cap_net_raw+ep .venv/bin/python3"
fi
echo "========================"
