# Skyport

A self-hosted, censorship-resistant proxy panel built on Xray-core with Cloudflare CDN fronting and WARP egress. Designed to resist passive traffic analysis, active probing, and ML-based classification.

## Features

- VLESS+XHTTP tunneled through Cloudflare CDN
- Cloudflare WARP as outbound egress (toggleable)
- Automatic TLS via Caddy + Cloudflare DNS
- Web UI with QR code and VLESS link generation
- S3/MinIO facade for GFW active probe resistance
- Single container deployment

## Requirements

- A domain managed by Cloudflare
- A Cloudflare auth token with `Zone.DNS Edit` and `Zone.Zone Read` permissions
- Docker and Docker Compose
- A VPS with `NET_ADMIN` capability (required for WARP/TUN)

## Notes

- **WARP toggle requires `ENABLE_WARP` to be set in `.env`** — if the variable is missing or commented out, the WARP toggle in the web UI will not work. This is a known limitation.

## Installation

### 1. Create directory structure

```bash
mkdir skyport && \
cd skyport && \
mkdir -p config/{certs,caddy_config,xray_config/xray_core,xray_config/db} && \
touch docker-compose.yaml && \
touch .env
```

### 2. Create `docker-compose.yml`

There are two available images — pick one:

| Image | Description |
|---|---|
| `xia1997x/skyport:staging` | Full version with web UI. Requires `SKYPORT_USERNAME` and `SKYPORT_PASSWORD`. |
| `xia1997x/skyport-headless:staging` | No web UI. `SKYPORT_USERNAME` and `SKYPORT_PASSWORD` are not needed. |

**With web UI:**

```yaml
services:
  skyport:
    image: xia1997x/skyport:staging
    container_name: skyport
    restart: always
    env_file:
      - .env
    ports:
      - '$PORT:443'
    cap_add:
      - NET_ADMIN
    devices:
      - /dev/net/tun:/dev/net/tun
    volumes:
      - ./config/certs:/xray_base/caddy_certs
      - ./config/caddy_config:/xray_base/backend/caddy_config
      - ./config/xray_config:/xray_base/backend/xray_config/
      - ./config/xray_config/db:/xray_base/backend/xray_config/db
      - ./config/xray_config/xray_core:/xray_base/backend/xray_config/xray_core
```

**Headless (no web UI):**

```yaml
services:
  skyport:
    image: xia1997x/skyport-headless:staging
    container_name: skyport
    restart: always
    env_file:
      - .env
    ports:
      - '$PORT:443'
    cap_add:
      - NET_ADMIN
    devices:
      - /dev/net/tun:/dev/net/tun
    volumes:
      - ./config/certs:/xray_base/caddy_certs
      - ./config/caddy_config:/xray_base/backend/caddy_config
      - ./config/xray_config:/xray_base/backend/xray_config/
      - ./config/xray_config/db:/xray_base/backend/xray_config/db
      - ./config/xray_config/xray_core:/xray_base/backend/xray_config/xray_core
```

### 3. Create `.env`

```env
DOMAIN_NAME=your.domain.com
CLOUDFLARE_AUTH_TOKEN=your_cloudflare_api_token
PORT=8443
ENABLE_CADDY_LOG=False
ENABLE_WARP=True
XRAY_VERSION=latest
SKYPORT_USERNAME=admin
SKYPORT_PASSWORD=changeme
# XRAY_UUID=
# XRAY_PATH=
```

| Variable | Description |
|---|---|
| `DOMAIN_NAME` | Your domain managed by Cloudflare |
| `CLOUDFLARE_AUTH_TOKEN` | Cloudflare auth token with `Zone.DNS Edit` and `Zone.Zone Read` permissions |
| `PORT` | Host port to expose (maps to container port 443) |
| `ENABLE_CADDY_LOG` | Enable Caddy access logs (`True`/`False`) |
| `ENABLE_WARP` | Use Cloudflare WARP as outbound egress (`True`/`False`) |
| `XRAY_VERSION` | Xray-core version to use (`latest` or a specific version tag) |
| `SKYPORT_USERNAME` | Web UI login username |
| `SKYPORT_PASSWORD` | Web UI login password |
| `XRAY_UUID` | ⚠️ Optional, for testing only. Overrides the auto-generated Xray UUID. If unset, a UUID is generated automatically. |
| `XRAY_PATH` | ⚠️ Optional, for testing only. Overrides the auto-generated Xray path. Must be lowercase and contain only letters, numbers, and `-`. If unset, a random path is generated. |

### 4. Start

```bash
docker compose up -d
```

Caddy will automatically obtain a TLS certificate via Cloudflare DNS challenge on first startup. Once the container is running, fetch your dashboard URL and VLESS link from the logs:

```bash
docker compose logs skyport | grep -E "DASHBOARD URL|https|VLESS CONNECTION LINK|vless"
```

## Cloudflare Setup

1. Your domain must use Cloudflare as its DNS provider
2. Create an API token with `Zone.DNS Edit` and `Zone.Zone Read` permissions scoped to your domain
3. In Cloudflare, set your domain's proxy status to **Proxied** (orange cloud) — this is what enables CDN fronting

## Updating

```bash
docker compose pull
docker compose up -d
```