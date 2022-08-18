# normalizes a MAC address by removing all non alphanumeric and uppercasing all characters
function normalize_mac() {
  local mac=$1
  echo "$mac" | tr -d ":" | tr -d "-" |  tr "[:lower:]" "[:upper:]"
}


set -e

# Print usage
if [ $# -lt 1 ]; then
    echo "Not enough arguments provided!"
    echo "This script gets the redirector URL for an AP identified by the provided MAC address."
    echo "Usage: $0 <mac-address>"
    echo "mac-address - the primary MAC address of your AP device"
    exit 1
fi

mac="$(normalize_mac "$1")"

device_details=$(curl \
  --silent \
  --request GET "${DIGICERT_BASE_URL}v2/device?limit=1&device_identifier=${mac}" \
  --header "x-api-key: $DIGICERT_API_KEY" | jq --raw-output .records[0])

current_fields=$(echo "$device_details" | jq --raw-output .fields)

echo "$current_fields" | jq --raw-output '.[] | select( .name == "Redirector" ) | .value'