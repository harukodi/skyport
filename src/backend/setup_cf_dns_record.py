import sys
import cloudflare
from urllib.request import urlopen
from cloudflare import Cloudflare
from vars import cloudflare_auth_token, domain_name

class DnsRecordDoesNotExist(Exception):
    pass

cf_client = Cloudflare(
    api_token=cloudflare_auth_token
)

def verify_cf_api_token():
    try:
        cf_client.user.tokens.verify()
        return True
    except Exception:
        return False

def fetch_public_ip():
    ip_api_endpoint = "https://checkip.amazonaws.com/"
    response = urlopen(ip_api_endpoint)
    ip_data = response.read().decode("utf-8").strip()
    return ip_data

def fetch_zone_id():
    main_domain_name = ".".join(domain_name.split(".")[-2:])
    zone_ids = cf_client.zones.list()
    for zone_id in zone_ids:
        if zone_id.name == main_domain_name:
            return zone_id.id

def fetch_dns_record_id(zone_id):
    dns_records = cf_client.dns.records.list(
        zone_id=zone_id
    )
    for dns_record in dns_records:
        if dns_record.name == domain_name:
            return dns_record.id

def delete_existing_dns_record(zone_id):
    dns_record_id = fetch_dns_record_id(zone_id)
    if not dns_record_id:
        raise DnsRecordDoesNotExist
    
    cf_client.dns.records.delete(
        dns_record_id=dns_record_id,
        zone_id=zone_id,
    )

def create_dns_record(zone_id):
    cf_client.dns.records.create(
        zone_id=zone_id,
        content=fetch_public_ip(),
        name=domain_name,
        proxied=True,
        type="A"
    )

def setup_dns_record():
    zone_id = fetch_zone_id()
    try:
        if verify_cf_api_token():
            delete_existing_dns_record(zone_id)
            create_dns_record(zone_id)
            print(f"DNS record for {domain_name} has been updated.")
        else:
            print("Invalid Cloudflare API token or insufficient permissions.")
            sys.exit(1)
    except DnsRecordDoesNotExist:
        create_dns_record(zone_id)
        print(f"DNS record for {domain_name} has been created.")
    except cloudflare.APIStatusError as e:
        error_message = e.errors[0].message.rstrip(".")
        if e.status_code == 400:
            print(f"{error_message} for {domain_name}.")
            print("Continuing...")
        else:
            print(f"Error {e.status_code}: {error_message}")
            sys.exit(1)