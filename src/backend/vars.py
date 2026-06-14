import uuid, string, random
from os import environ
from dotenv import load_dotenv
load_dotenv(override=True)

xray_uuid = environ.get("XRAY_UUID", str(uuid.uuid4()))
xray_path = environ.get("XRAY_PATH", ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=38)))
xray_encryption_key = environ.get("XRAY_ENCRYPTION_KEY", None)
xray_decryption_key = environ.get("XRAY_DECRYPTION_KEY", None)
domain_name = environ.get("DOMAIN_NAME")
port = environ.get("PORT", "443")
xray_version = environ.get("XRAY_VERSION", "latest")
wgcf_version = environ.get("WGCF_VERSION", "latest")
cloudflare_auth_token = environ.get("CLOUDFLARE_AUTH_TOKEN")
enable_caddy_log = environ.get("ENABLE_CADDY_LOG", "False")
enable_warp = environ.get("ENABLE_WARP", "True")
