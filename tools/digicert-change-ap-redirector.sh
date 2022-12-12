# normalizes a MAC address by removing all non alphanumeric and uppercasing all characters
function normalize_mac() {
  local mac=$1
  echo "$mac" | tr -d ":" | tr -d "-" |  tr "[:lower:]" "[:upper:]"
}

DIGICERT_BASE_URL="https://one.digicert.com/iot/api/"

set -e

# Print usage
if [ $# -lt 2 ]; then
    echo "Not enough arguments provided!"
    echo "This script changes the redirector URL for an AP identified by the provided MAC address."
    echo "Usage: $0 <mac-address> <redirector>"
    echo "mac-address - the primary MAC address of your AP device"
    echo "redirector - the new redirector URL"
    exit 1
fi

mac="$(normalize_mac "$1")"
redirector="$2"

device_details=$(curl \
  --silent \
  --request GET "${DIGICERT_BASE_URL}v2/device?limit=1&device_identifier=${mac}" \
  --header "x-api-key: $DIGICERT_API_KEY" | jq --raw-output .records[0])

device_id=$(echo "$device_details" | jq --raw-output .id)
current_fields=$(echo "$device_details" | jq --raw-output .fields)
new_fields=$(echo "$current_fields" | jq --raw-output "(.[] | select(.name == \"Redirector\") | .value) |= \"$redirector\"")

curl \
  --request PUT "${DIGICERT_BASE_URL}v2/device/$device_id" \
  --header "x-api-key: $DIGICERT_API_KEY" -H "Content-Type: application/json" -d "{\"fields\":$new_fields}"