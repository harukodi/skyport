files_to_remove=(
    "src/app/caddy_config/*"
    "src/app/xray_config/xray_config.json"
    "src/app/xray_config/xray_client_vless_link.json"
    "src/app/xray_config/xray_client_qr_code.png"
    "src/app/xray_config/xray_core/*"
    "tests/client_config.json"
    "tests/infrastructure/xray_server_config/config"
    "tests/infrastructure/xray_server_config/.public.env"
)

function remove_file () {
    file_to_remove="$1"
    rm -rf $file_to_remove
}

for file in "${files_to_remove[@]}"
do
    remove_file "$file"
done