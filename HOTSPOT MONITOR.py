import scapy.all as scapy
import subprocess
import time
import threading
from collections import defaultdict
from blessed import Terminal

term = Terminal()

# Dictionary to store data transfer per device
device_traffic = defaultdict(lambda: {"sent": 0, "received": 0})

def get_connected_devices():
    """Uses nmap to find connected devices on the local network."""
    devices = []
    result = subprocess.run(["nmap", "-sn", "192.168.1.0/24"], capture_output=True, text=True)
    
    # Extract IP and MAC addresses
    lines = result.stdout.split("\n")
    ip, mac = None, None
    for line in lines:
        if "Nmap scan report for" in line:
            ip = line.split(" ")[-1]
        if "MAC Address" in line:
            parts = line.split(" ")
            mac = parts[2]
            vendor = " ".join(parts[3:]) if len(parts) > 3 else "Unknown"
            devices.append({"IP": ip, "MAC": mac, "Vendor": vendor})
    return devices

def packet_callback(packet):
    """Tracks data sent/received per IP address."""
    if packet.haslayer(scapy.IP):
        src_ip = packet[scapy.IP].src
        dst_ip = packet[scapy.IP].dst
        packet_size = len(packet)

        device_traffic[src_ip]["sent"] += packet_size
        device_traffic[dst_ip]["received"] += packet_size

def monitor_network():
    """Sniffs network traffic in the background."""
    scapy.sniff(prn=packet_callback, store=False)

def display_dashboard():
    """Real-time CLI dashboard using blessed."""
    while True:
        print(term.clear)
        print(term.bold("📡 Connected Devices & Data Usage"))
        print(term.yellow("IP Address        MAC Address        Vendor       Upload (B/s)   Download (B/s)"))
        print("-" * 80)

        devices = get_connected_devices()
        for device in devices:
            ip = device["IP"]
            mac = device["MAC"]
            vendor = device["Vendor"]
            upload_rate = device_traffic[ip]["sent"] / 2
            download_rate = device_traffic[ip]["received"] / 2
            
            print(f"{ip:<16} {mac:<18} {vendor:<12} {upload_rate:<12.2f} {download_rate:<12.2f}")

            # Reset counters for next update
            device_traffic[ip] = {"sent": 0, "received": 0}

        time.sleep(2)

# Start network monitoring in background
threading.Thread(target=monitor_network, daemon=True).start()

# Launch the CLI dashboard
display_dashboard()
