#!/usr/bin/env python3
import os, json, requests

API_KEY = os.environ["TAILSCALE_API_KEY"]
TAILNET = os.environ.get("TAILSCALE_TAILNET", "-")  # "-" means the user’s default tailnet (API key owner)

url = f"https://api.tailscale.com/api/v2/tailnet/{TAILNET}/devices"
headers = {"Authorization": f"Bearer {API_KEY}"}

resp = requests.get(url, headers=headers)
resp.raise_for_status()
devices = resp.json()["devices"]

online = []
for d in devices:
    if d.get("online"):
        # Grab the first Tailscale IPv4 address (usually the 100.x.y.z one)
        ts_ips = d.get("addresses", [])
        ts_ip = next((ip for ip in ts_ips if ip.startswith("100.")), ts_ips[0] if ts_ips else "")

        online.append({
            "name": d.get("hostname", d["name"]),
            "hostname": d.get("name"),          # full MagicDNS name (if MagicDNS enabled)
            "ip": ts_ip,
            "os": d.get("os", ""),
            "user": d.get("user", ""),
            "lastSeen": d.get("lastSeen", "")
        })

with open("devices.json", "w") as f:
    json.dump(online, f, indent=2)

print(f"✅ Saved {len(online)} online devices")
