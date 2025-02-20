UPDATE 1:
Approach:
Basic Python script that detects connected devices using arp-scan or nmap. It will list the IP address, MAC address, and hostname of each connected device.
Dependencies:
You'll need to install nmap (or arp-scan)

UPDATE 2:
Approach:
Use scapy or iptables/netstat to track data packets per device.
Calculate bytes sent/received per second to determine transfer rates.
Display real-time updates.
Dependencies:
Install scapy and psutil if you don’t have them:

UPDATE 3:
Approach:
Detects connected devices using nmap.
Tracks upload/download speed per device.
Displays a real-time CLI dashboard with automatic updates.
Uses blessed for smooth, flicker-free terminal UI.
Dependencies:
Install blessed
