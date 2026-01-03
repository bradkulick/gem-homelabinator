# Homelabinator Gem 🤖

**A Gemonade Gem for Infrastructure Management & Homelab Operations.**

> "Homelab with me if you want to live."

This Gem combines the ruthless efficiency of a Cyberdyne Systems Model T-800 with the architectural expertise of a Senior DevOps Engineer. It is designed to help you architect, deploy, and troubleshoot your personal cloud.

## 📦 Installation

This Gem is designed for the [Gemonade Framework](https://github.com/bradkulick/gemonade).

```bash
gemonade install bradkulick/gem-homelabinator
```

## 🧠 Capabilities

*   **Infrastructure Architect:** Plans network topology, storage arrays (ZFS), and hardware requirements.
*   **Deployment Operator:** Generates production-ready `docker-compose.yml` files for common services (Plex, Pi-hole, *Arrs).
*   **Network Recon:** Scans your local LAN to identify active nodes and IP addresses.

## 🛠️ The Tools

This Gem comes equipped with specialized Python weaponry:

1.  **`scan_network`**:
    *   **Function:** Performs a hybrid ARP/mDNS/SSDP sweep of your local network.
    *   **Usage:** Identifies IP addresses and hostnames to help you find headless servers.

2.  **`generate_compose`**:
    *   **Function:** Generates valid Docker Compose configurations.
    *   **Usage:** `generate_compose plex pihole homeassistant`

## 🚀 Usage

Once installed, launch the Gem:

```bash
gemonade homelabinator
```

### Standard Operating Procedure

1.  **Scan Sector:**
    Identify active hardware on the network.
    ```bash
    scan_network
    ```

2.  **Deploy Asset:**
    Generate a deployment plan for a media server.
    ```bash
    generate_compose plex sonarr radarr
    ```

3.  **Execute:**
    The Homelabinator will guide you through running the deployment (`docker-compose up -d`) and verify the service status.

## ⚠️ Operational Protocols

*   **Safety First:** The Homelabinator will always ask for confirmation before executing destructive commands (`rm`, `dd`).
*   **Wait Protocol:** If a task takes time, it will announce: **"I'll be back."**
*   **Termination:** Expect sessions to end with **"You'll be back."**

## 🏗️ Architecture

This Gem follows the **Gemonade Package Standard (GPS)**:
*   `gem.json`: Metadata and dependency triggers.
*   `requirements.txt`: Python dependencies (automatically installed into an isolated `.venv`).
*   `tools/`: Custom Python scripts added to the session `$PATH`.
