import subprocess
import re

def get_connected_devices():
    devices = []
    
    # Run nmap to scan the local network
    result = subprocess.run(["nmap", "-sn", "192.168.1.0/24"], capture_output=True, text=True)
    
    # Extract IP and MAC addresses
    matches = re.findall(r"Nmap scan report for (.*?)\n.*?MAC Address: (.*?) \((.*?)\)", result.stdout, re.DOTALL)

    for match in matches:
        ip, mac, vendor = match
        devices.append({"IP": ip, "MAC": mac, "Vendor": vendor})

    return devices

if __name__ == "__main__":
    devices = get_connected_devices()
    print("\nConnected Devices:")
    print("IP Address\t\tMAC Address\t\tVendor")
    for device in devices:
        print(f"{device['IP']}\t{device['MAC']}\t{device['Vendor']}")
