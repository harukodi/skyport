from vars import domain_name, xray_path
from string import Template

caddyfile_template = "./templates/caddyfile_template"
output_caddyfile = "./caddy_config/Caddyfile"

def generate_caddy_config():
    caddyfile_substitute_values = {
        "domain_name": domain_name,
        "xray_path": xray_path  
    }

    with open(caddyfile_template, 'r') as file:
        caddyfile = file.read()
        caddyfile_substituted = Template(caddyfile).substitute(caddyfile_substitute_values)
    
    with open(output_caddyfile, 'w') as file:
        file.write(caddyfile_substituted)