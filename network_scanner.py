# Example: assign the filename to a variable
filename = "network scanner project" \

import socket
import ipaddress
from concurrent.futures import ThreadPoolExecutor
SUBNET = "192.168.1.0/24"
PORTS_TO_SCAN = [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 445, 3306, 3389]

def is_host_alive(ip):
    try:
        socket.gethostbyaddr(str(ip))
        return str(ip)
    except socket.herror:
        return None

def scan_ports(ip):
    open_ports = []
    for port in PORTS_TO_SCAN:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            result = s.connect_ex((ip, port))
            if result == 0:
                open_ports.append(port)
    return open_ports

def main():
    print(f"\n[+] Scanning network: {SUBNET}")
    network = ipaddress.ip_network(SUBNET, strict=False)
    live_hosts = []

    with ThreadPoolExecutor(max_workers=100) as executor:
        results = executor.map(is_host_alive, network.hosts())
        for ip in results:
            if ip:
                print(f"[✓] Host active: {ip}")
                live_hosts.append(ip)

    print("\n[+] Starting port scan on active hosts...")
    for ip in live_hosts:
        open_ports = scan_ports(ip)
        if open_ports:
            print(f"[→] {ip} has open ports: {open_ports}")
        else:
            print(f"[→] {ip} has no common open ports.")

if __name__ == "__main__":
    main()


