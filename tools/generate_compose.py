#!/usr/bin/env python3
import sys
import argparse
import yaml

# --- Templates ---

TEMPLATES = {
    "plex": {
        "image": "lscr.io/linuxserver/plex:latest",
        "container_name": "plex",
        "network_mode": "host",
        "environment": [
            "PUID=1000",
            "PGID=1000",
            "VERSION=docker"
        ],
        "volumes": [
            "./plex/config:/config",
            "/path/to/tvseries:/tv",
            "/path/to/movies:/movies"
        ],
        "restart": "unless-stopped"
    },
    "pihole": {
        "container_name": "pihole",
        "image": "pihole/pihole:latest",
        "ports": [
            "53:53/tcp",
            "53:53/udp",
            "67:67/udp",
            "80:80/tcp"
        ],
        "environment": {
            "TZ": "UTC",
            "WEBPASSWORD": "admin"
        },
        "volumes": [
            "./etc-pihole:/etc/pihole",
            "./etc-dnsmasq.d:/etc/dnsmasq.d"
        ],
        "cap_add": ["NET_ADMIN"],
        "restart": "unless-stopped"
    },
    "homeassistant": {
        "container_name": "homeassistant",
        "image": "ghcr.io/home-assistant/home-assistant:stable",
        "volumes": [
            "./homeassistant/config:/config",
            "/etc/localtime:/etc/localtime:ro"
        ],
        "restart": "unless-stopped",
        "privileged": True,
        "network_mode": "host"
    },
    "nginx-proxy-manager": {
        "image": "jc21/nginx-proxy-manager:latest",
        "container_name": "nginx-proxy-manager",
        "restart": "unless-stopped",
        "ports": [
            "80:80",
            "81:81",
            "443:443"
        ],
        "volumes": [
            "./npm/data:/data",
            "./npm/letsencrypt:/etc/letsencrypt"
        ]
    },
    "adguard-home": {
        "image": "adguard/adguardhome",
        "container_name": "adguardhome",
        "restart": "unless-stopped",
        "ports": [
            "53:53/tcp", "53:53/udp",
            "784:784/udp", "853:853/tcp", "853:853/udp",
            "3000:3000/tcp", "80:80/tcp", "443:443/tcp", "443:443/udp"
        ],
        "volumes": [
            "./adguard/work:/opt/adguardhome/work",
            "./adguard/conf:/opt/adguardhome/conf"
        ]
    }
}

# --- Logic ---

def generate_compose(services):
    compose = {
        "version": "3.8",
        "services": {}
    }
    
    for service in services:
        if service.lower() in TEMPLATES:
            compose["services"][service.lower()] = TEMPLATES[service.lower()]
        else:
            print(f"[-] Warning: No template for '{service}'. Adding placeholder.")
            compose["services"][service.lower()] = {
                "image": f"{service}:latest",
                "container_name": service,
                "restart": "unless-stopped"
            }
            
    return yaml.dump(compose, sort_keys=False)

def main():
    parser = argparse.ArgumentParser(description="Generate a docker-compose.yml for common homelab services.")
    parser.add_argument("services", nargs="+", help="List of services to include (e.g., plex pihole)")
    parser.add_argument("-o", "--output", default="docker-compose.yml", help="Output file (default: docker-compose.yml)")
    
    args = parser.parse_args()
    
    print(f"[*] Drafting attack plan for services: {', '.join(args.services)}")
    
    yaml_content = generate_compose(args.services)
    
    try:
        with open(args.output, "w") as f:
            f.write(yaml_content)
        print(f"[+] Composition complete. File saved to: {args.output}")
    except Exception as e:
        print(f"[-] Error writing file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
