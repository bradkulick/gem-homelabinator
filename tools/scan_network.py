#!/usr/bin/env python3
import subprocess
import re
import socket
import time
import threading
import ipaddress
import argparse
import sys

def get_my_ip_info():
    try:
        res = subprocess.check_output(["ip", "-o", "-4", "addr", "show", "up"]).decode()
        for line in res.splitlines():
            if " lo " in line: continue
            match = re.search(r"inet\s+(\d+\.\d+\.\d+\.\d+)/(\d+)", line)
            if match:
                return match.group(1), int(match.group(2))
    except: pass
    return None, None

def ping_host(ip):
    try:
        subprocess.call(["ping", "-c", "1", "-W", "1", str(ip)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except: pass

def active_scan():
    my_ip, cidr = get_my_ip_info()
    if not my_ip:
        return []

    network = ipaddress.IPv4Network(f"{my_ip}/{cidr}", strict=False)
    
    threads = []
    # Limit to /24 for speed and safety in a homelab context
    hosts = list(network.hosts())
    if len(hosts) > 256:
        hosts = hosts[:256]

    for ip in hosts:
        if str(ip) == my_ip: continue
        t = threading.Thread(target=ping_host, args=(ip,))
        t.start()
        threads.append(t)
    for t in threads: t.join()

    results = []
    try:
        res = subprocess.check_output(["ip", "neigh"]).decode()
        for line in res.splitlines():
            parts = line.split()
            if len(parts) >= 5 and "lladdr" in parts:
                ip = parts[0]
                mac = parts[parts.index("lladdr") + 1].upper()
                results.append({"ip": ip, "mac": mac, "source": "ARP"})
    except: pass
    return results

def passive_scan(timeout=3):
    devices = {}

    def scan_ssdp():
        addr, port = "239.255.255.250", 1900
        req = (f"M-SEARCH * HTTP/1.1\r\nHOST: {addr}:{port}\r\nMAN: \"ssdp:discover\"\r\nMX: 2\r\nST: ssdp:all\r\n\r\n").encode()
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(timeout)
            for _ in range(2): sock.sendto(req, (addr, port))
            start = time.time()
            while time.time() - start < timeout:
                try:
                    data, addr_info = sock.recvfrom(65535)
                    decoded = data.decode('utf-8', errors='ignore')
                    headers = {l.split(':', 1)[0].upper(): l.split(':', 1)[1].strip() for l in decoded.split('\r\n') if ':' in l}
                    server = headers.get('SERVER', 'Unknown')
                    devices[addr_info[0]] = {"info": f"SSDP: {server}"}
                except socket.timeout: break
        except: pass

    def listen_mdns():
        addr, port = "224.0.0.251", 5353
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind(("", port))
            sock.settimeout(timeout)
            start = time.time()
            while time.time() - start < timeout:
                try:
                    data, addr_info = sock.recvfrom(65535)
                    content = "".join([c if c.isprintable() else '.' for c in data.decode('utf-8', errors='ignore')])
                    matches = re.findall(r'[\w-]+\.local', content)
                    if matches:
                        existing = devices.get(addr_info[0], {"info": ""})
                        new_info = f"mDNS: {', '.join(set(matches))}"
                        devices[addr_info[0]] = {"info": f"{existing['info']} {new_info}".strip()}
                except socket.timeout: break
        except: pass

    t1 = threading.Thread(target=scan_ssdp)
    t2 = threading.Thread(target=listen_mdns)
    t1.start(); t2.start()
    t1.join(); t2.join()
    
    return [{"ip": ip, "info": d["info"]} for ip, d in devices.items()]

def main():
    parser = argparse.ArgumentParser(description="Scan local network for devices (ARP + mDNS + SSDP).")
    parser.add_argument("--timeout", type=int, default=3, help="Timeout for passive scanning (seconds)")
    args = parser.parse_args()

    print("[*] Initiating network infiltration...")
    print("[*] I'll be back.") # Wait Protocol
    
    found_devices = {}

    # 1. Passive Scan
    p_results = passive_scan(timeout=args.timeout)
    for d in p_results:
        found_devices[d['ip']] = {"mac": "Unknown", "info": d['info']}

    # 2. Active Scan
    a_results = active_scan()
    for d in a_results:
        if d['ip'] in found_devices:
            found_devices[d['ip']]["mac"] = d['mac']
        else:
            found_devices[d['ip']] = {"mac": d['mac'], "info": ""}

    # 3. Report
    print(f"\n[+] Scan Complete. Found {len(found_devices)} Unique Devices.")
    print(f"{ 'IP Address':<15} | { 'MAC Address':<17} | {'Information'}")
    print("-" * 75)
    
    for ip in sorted(found_devices.keys(), key=lambda x: ipaddress.IPv4Address(x)):
        data = found_devices[ip]
        mac = data['mac']
        info = data['info']
        print(f"{ip:<15} | {mac:<17} | {info}")

    print("-" * 75)
    print("You'll be back.")

if __name__ == "__main__":
    main()
