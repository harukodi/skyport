files_to_remove=(
    "src/backend/caddy_config/*"
    "src/backend/xray_config/xray_config.json"
    "src/backend/xray_config/xray_client_vless_link.json"
    "src/backend/xray_config/xray_client_qr_code.png"
    "src/backend/xray_config/xray_core/*"
    "src/frontend/assets/xray_data/*"
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