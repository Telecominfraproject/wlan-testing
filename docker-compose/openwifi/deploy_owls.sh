#!/bin/bash
set -e

# Usage function
usage () {
  echo;
  echo "This script is intended for OpenWifi OWLS deployment using Docker Compose (https://github.com/Telecominfraproject/wlan-cloud-ucentral-deploy/tree/main/docker-compose) in a Kubernetes pod";
  echo;
  echo "Required environment variables:"
  echo;
  echo "- DEPLOY_VERSION - version of the wlan-cloud-ucentral-deploy repo to be used";
  echo;
  echo "- DEFAULT_UCENTRALSEC_URL - public URL of the OWSec service"
  echo "- SYSTEM_URI_UI - public URL of the OWGW-UI service"
  echo;
  echo "- INTERNAL_OWSEC_HOSTNAME - OWSec microservice hostname for Docker internal communication"
  echo;
  echo "- OWSEC_SYSTEM_URI_PRIVATE - private URL to be used for OWSec";
  echo "- OWSEC_SYSTEM_URI_PUBLIC - public URL to be used for OWSec";
  echo "- OWSEC_AUTHENTICATION_DEFAULT_USERNAME - username to be used for requests to OWSec";
  echo "- OWSEC_AUTHENTICATION_DEFAULT_PASSWORD - hashed password for OWSec (details on this may be found in https://github.com/Telecominfraproject/wlan-cloud-ucentralsec/#authenticationdefaultpassword)";
  echo;
  echo "- OWLS_SYSTEM_URI_PRIVATE - private URL to be used for OWLS";
  echo "- OWLS_SYSTEM_URI_PUBLIC - public URL to be used for OWLS";
  echo;
  echo "- DEVICE_CERT - path to the device certificate";
  echo "- DEVICE_KEY - path to the device key";
}

# Check if required environment variables were passed
## Deployment specifics
[ -z ${DEPLOY_VERSION+x} ] && echo "DEPLOY_VERSION is unset" && usage && exit 1
## Configuration variables applying to multiple microservices
[ -z ${DEFAULT_UCENTRALSEC_URL+x} ] && echo "DEFAULT_UCENTRALSEC_URL is unset" && usage && exit 1
[ -z ${SYSTEM_URI_UI+x} ] && echo "SYSTEM_URI_UI is unset" && usage && exit 1
## Internal microservice hostnames
[ -z ${INTERNAL_OWSEC_HOSTNAME+x} ] && echo "INTERNAL_OWSEC_HOSTNAME is unset" && usage && exit 1
## OWSec configuration variables
[ -z ${OWSEC_AUTHENTICATION_DEFAULT_USERNAME+x} ] && echo "OWSEC_AUTHENTICATION_DEFAULT_USERNAME is unset" && usage && exit 1
[ -z ${OWSEC_AUTHENTICATION_DEFAULT_PASSWORD+x} ] && echo "OWSEC_AUTHENTICATION_DEFAULT_PASSWORD is unset" && usage && exit 1
[ -z ${OWSEC_SYSTEM_URI_PRIVATE+x} ] && echo "OWSEC_SYSTEM_URI_PRIVATE is unset" && usage && exit 1
[ -z ${OWSEC_SYSTEM_URI_PUBLIC+x} ] && echo "OWSEC_SYSTEM_URI_PUBLIC is unset" && usage && exit 1
# OWLS configuration variables
[ -z ${OWLS_SYSTEM_URI_PRIVATE+x} ] && echo "OWLS_SYSTEM_URI_PRIVATE is unset" && usage && exit 1
[ -z ${OWLS_SYSTEM_URI_PUBLIC+x} ] && echo "OWLS_SYSTEM_URI_PUBLIC is unset" && usage && exit 1
## cert related variables
[ -z ${DEVICE_CERT+x} ] && echo "DEVICE_CERT is unset" && usage && exit 1
[ -z ${DEVICE_KEY+x} ] && echo "DEVICE_KEY is unset" && usage && exit 1

# Clone repo and copy certificates
mkdir wlan-cloud-ucentral-deploy-tmp
git clone --branch $DEPLOY_VERSION https://github.com/Telecominfraproject/wlan-cloud-ucentral-deploy.git /wlan-cloud-ucentral-deploy-tmp 
mv -f /wlan-cloud-ucentral-deploy-tmp/* /wlan-cloud-ucentral-deploy/ && rm -r wlan-cloud-ucentral-deploy-tmp
cd wlan-cloud-ucentral-deploy/docker-compose/owls

# Search and replace variable values in env files
sed -i "s~\(^INTERNAL_OWSEC_HOSTNAME=\).*~\1$INTERNAL_OWSEC_HOSTNAME~" .env
sed -i "s~\(^INTERNAL_OWLS_HOSTNAME=\).*~\1$INTERNAL_OWLS_HOSTNAME~" .env

sed -i "s~\(^DEFAULT_UCENTRALSEC_URL=\).*~\1$DEFAULT_UCENTRALSEC_URL~" owls-ui.env

sed -i "s~.*AUTHENTICATION_DEFAULT_USERNAME=.*~AUTHENTICATION_DEFAULT_USERNAME=$OWSEC_AUTHENTICATION_DEFAULT_USERNAME~" owsec.env
sed -i "s~.*AUTHENTICATION_DEFAULT_PASSWORD=.*~AUTHENTICATION_DEFAULT_PASSWORD=$OWSEC_AUTHENTICATION_DEFAULT_PASSWORD~" owsec.env
sed -i "s~\(^SYSTEM_URI_PRIVATE=\).*~\1$OWSEC_SYSTEM_URI_PRIVATE~" owsec.env
sed -i "s~\(^SYSTEM_URI_PUBLIC=\).*~\1$OWSEC_SYSTEM_URI_PUBLIC~" owsec.env
sed -i "s~\(^SYSTEM_URI_UI=\).*~\1$SYSTEM_URI_UI~" owsec.env

sed -i "s~\(^SYSTEM_URI_PRIVATE=\).*~\1$OWLS_SYSTEM_URI_PRIVATE~" owls.env
sed -i "s~\(^SYSTEM_URI_PUBLIC=\).*~\1$OWLS_SYSTEM_URI_PUBLIC~" owls.env

# Run the deployment and attach to logs
cat $DEVICE_CERT > ../certs/device-cert.pem
cat $DEVICE_KEY > ../certs/device-key.pem
exec docker-compose up --attach-dependencies
