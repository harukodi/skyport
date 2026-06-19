# Build caddy with cloudflare plugin
ARG PYTHON_VERSION=3.13.11-slim-trixie
ARG CADDY_BUILDER_VERSION=2.10.2-builder-alpine
ARG CADDY_SERVER_VERSION=2.10.2-alpine
ARG CLOUDFLARE_WARP_INSTALLER_IMAGE=trixie-slim

# Build step for caddy web server
FROM caddy:${CADDY_BUILDER_VERSION} AS caddy_builder
RUN xcaddy build \
    --with github.com/caddy-dns/cloudflare
FROM caddy:${CADDY_SERVER_VERSION}

# Install step for cloudflare-warp
FROM debian:${CLOUDFLARE_WARP_INSTALLER_IMAGE} AS cloudflare_warp_installer
RUN apt update && apt install ca-certificates curl gnupg2 lsb-release libcap2-bin gosu binutils -y --no-install-recommends && \
    curl -fsSL https://pkg.cloudflareclient.com/pubkey.gpg | gpg --yes --dearmor --output /usr/share/keyrings/cloudflare-warp-archive-keyring.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/cloudflare-warp-archive-keyring.gpg] https://pkg.cloudflareclient.com/ $(lsb_release -cs) main" | tee /etc/apt/sources.list.d/cloudflare-client.list && \
    apt update && apt install cloudflare-warp --no-install-recommends -y && \
    strip --strip-unneeded /usr/bin/warp-cli && \
    strip --strip-unneeded /usr/bin/warp-svc

# Backend stage
FROM python:${PYTHON_VERSION} AS backend
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive
ENV XDG_DATA_HOME=/xray_base/caddy_certs
ENV SKYPORT_UI=false
EXPOSE 443/tcp
EXPOSE 443/udp
COPY --from=caddy_builder /usr/bin/caddy /usr/bin/caddy
COPY --from=cloudflare_warp_installer /usr/bin/warp-cli /usr/bin/warp-cli
COPY --from=cloudflare_warp_installer /usr/bin/warp-svc /usr/bin/warp-svc
COPY --from=cloudflare_warp_installer /usr/sbin/setcap /usr/sbin/setcap
COPY --from=cloudflare_warp_installer /usr/sbin/gosu /usr/sbin/gosu
COPY backend/ /xray_base/backend
COPY packages/ /xray_base/packages
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
WORKDIR /xray_base

RUN apt update && apt install dbus iproute2 nftables libpcap0.8 libnspr4 libnss3 --no-install-recommends -y && \
    apt clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* && \
    rm -rf /usr/share/doc /usr/share/man /usr/share/locale && \
    rm -rf /usr/bin/apt /usr/bin/apt-get && \
    rm -rf /usr/bin/dpkg /usr/bin/dpkg-deb

RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=backend/requirements.txt,target=requirements.txt \
    python -m pip install -r backend/requirements.txt && \
    python -m pip install -e ./packages && \
    mkdir /xray_base/caddy_certs /run/dbus && \
    chmod +x /usr/bin/caddy && \
    setcap cap_net_bind_service=+ep /usr/bin/caddy && \
    chmod +x /usr/local/bin/entrypoint.sh
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

# Frontend stage
FROM backend AS frontend
COPY frontend/ /xray_base/frontend
ENV SKYPORT_UI=true
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=frontend/requirements.txt,target=requirements.txt \
    python -m pip install -r frontend/requirements.txt && \
    python -m pip install -e ./packages
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]