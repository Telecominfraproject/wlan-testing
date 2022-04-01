#!/bin/bash
set -e

# Usage function
usage () {
  echo;
  echo "This script is intended for OpenWifi deployment using Docker Compose (https://github.com/Telecominfraproject/wlan-cloud-ucentral-deploy/tree/main/docker-compose) in a Kubernetes pod";
  echo;
  echo "Required environment variables:"
  echo;
  echo "- DEPLOY_VERSION - version of the wlan-cloud-ucentral-deploy repo to be used";
  echo;
  echo "- DEFAULT_UCENTRALSEC_URL - public URL of the OWSec service"
  echo "- SYSTEM_URI_UI - public URL of the OWGW-UI service"
  echo;
  echo "- INTERNAL_OWGW_HOSTNAME - OWGW microservice hostname for Docker internal communication"
  echo "- INTERNAL_OWSEC_HOSTNAME - OWSec microservice hostname for Docker internal communication"
  echo "- INTERNAL_OWFMS_HOSTNAME - OWFms microservice hostname for Docker internal communication"
  echo "- INTERNAL_OWPROV_HOSTNAME - OWProv microservice hostname for Docker internal communication"
  echo "- INTERNAL_OWANALYTICS_HOSTNAME - OWAnalytics microservice hostname for Docker internal communication"
  echo "- INTERNAL_OWSUB_HOSTNAME - OWSub microservice hostname for Docker internal communication"
  echo;
  echo "- OWGW_FILEUPLOADER_HOST_NAME - hostname to be used for OWGW fileupload";
  echo "- OWGW_FILEUPLOADER_URI - URL to be used for OWGW fileupload";
  echo "- OWGW_SYSTEM_URI_PRIVATE - private URL to be used for OWGW";
  echo "- OWGW_SYSTEM_URI_PUBLIC - public URL to be used for OWGW";
  echo "- OWGW_RTTY_SERVER - public hostname of the RTTY server";
  echo;
  echo "- OWSEC_SYSTEM_URI_PRIVATE - private URL to be used for OWSec";
  echo "- OWSEC_SYSTEM_URI_PUBLIC - public URL to be used for OWSec";
  echo "- OWSEC_AUTHENTICATION_DEFAULT_USERNAME - username to be used for requests to OWSec";
  echo "- OWSEC_AUTHENTICATION_DEFAULT_PASSWORD - hashed password for OWSec (details on this may be found in https://github.com/Telecominfraproject/wlan-cloud-ucentralsec/#authenticationdefaultpassword)";
  echo;
  echo "- OWFMS_SYSTEM_URI_PRIVATE - private URL to be used for OWFms";
  echo "- OWFMS_SYSTEM_URI_PUBLIC - public URL to be used for OWFms";
  echo "- OWFMS_S3_SECRET - secret key that is used for OWFms access to firmwares S3 bucket";
  echo "- OWFMS_S3_KEY - access key that is used for OWFms access to firmwares S3 bucket";
  echo;
  echo "- OWPROV_SYSTEM_URI_PRIVATE - private URL to be used for OWProv";
  echo "- OWPROV_SYSTEM_URI_PUBLIC - public URL to be used for OWProv";
  echo;
  echo "- OWANALYTICS_SYSTEM_URI_PRIVATE - private URL to be used for OWAnalytics";
  echo "- OWANALYTICS_SYSTEM_URI_PUBLIC - public URL to be used for OWAnalytics";
  echo;
  echo "- OWSUB_SYSTEM_URI_PRIVATE - private URL to be used for OWSub";
  echo "- OWSUB_SYSTEM_URI_PUBLIC - public URL to be used for OWSub";
  echo;
  echo "- WEBSOCKET_CERT - path to the websocket certificate";
  echo "- WEBSOCKET_KEY - path to the websocket key";
}

# Check if required environment variables were passed
## Deployment specifics
[ -z ${DEPLOY_VERSION+x} ] && echo "DEPLOY_VERSION is unset" && usage && exit 1
## Configuration variables applying to multiple microservices
[ -z ${DEFAULT_UCENTRALSEC_URL+x} ] && echo "DEFAULT_UCENTRALSEC_URL is unset" && usage && exit 1
[ -z ${SYSTEM_URI_UI+x} ] && echo "SYSTEM_URI_UI is unset" && usage && exit 1
## Internal microservice hostnames
[ -z ${INTERNAL_OWGW_HOSTNAME+x} ] && echo "INTERNAL_OWGW_HOSTNAME is unset" && usage && exit 1
[ -z ${INTERNAL_OWSEC_HOSTNAME+x} ] && echo "INTERNAL_OWSEC_HOSTNAME is unset" && usage && exit 1
[ -z ${INTERNAL_OWFMS_HOSTNAME+x} ] && echo "INTERNAL_OWFMS_HOSTNAME is unset" && usage && exit 1
[ -z ${INTERNAL_OWPROV_HOSTNAME+x} ] && echo "INTERNAL_OWPROV_HOSTNAME is unset" && usage && exit 1
[ -z ${INTERNAL_OWANALYTICS_HOSTNAME+x} ] && echo "INTERNAL_OWANALYTICS_HOSTNAME is unset" && usage && exit 1
[ -z ${INTERNAL_OWSUB_HOSTNAME+x} ] && echo "INTERNAL_OWSUB_HOSTNAME is unset" && usage && exit 1
## OWGW configuration variables
[ -z ${OWGW_FILEUPLOADER_HOST_NAME+x} ] && echo "OWGW_FILEUPLOADER_HOST_NAME is unset" && usage && exit 1
[ -z ${OWGW_FILEUPLOADER_URI+x} ] && echo "OWGW_FILEUPLOADER_URI is unset" && usage && exit 1
[ -z ${OWGW_SYSTEM_URI_PRIVATE+x} ] && echo "OWGW_SYSTEM_URI_PRIVATE is unset" && usage && exit 1
[ -z ${OWGW_SYSTEM_URI_PUBLIC+x} ] && echo "OWGW_SYSTEM_URI_PUBLIC is unset" && usage && exit 1
[ -z ${OWGW_RTTY_SERVER+x} ] && echo "OWGW_RTTY_SERVER is unset" && usage && exit 1
## OWSec configuration variables
[ -z ${OWSEC_AUTHENTICATION_DEFAULT_USERNAME+x} ] && echo "OWSEC_AUTHENTICATION_DEFAULT_USERNAME is unset" && usage && exit 1
[ -z ${OWSEC_AUTHENTICATION_DEFAULT_PASSWORD+x} ] && echo "OWSEC_AUTHENTICATION_DEFAULT_PASSWORD is unset" && usage && exit 1
[ -z ${OWSEC_SYSTEM_URI_PRIVATE+x} ] && echo "OWSEC_SYSTEM_URI_PRIVATE is unset" && usage && exit 1
[ -z ${OWSEC_SYSTEM_URI_PUBLIC+x} ] && echo "OWSEC_SYSTEM_URI_PUBLIC is unset" && usage && exit 1
## OWFms configuration variables
[ -z ${OWFMS_SYSTEM_URI_PRIVATE+x} ] && echo "OWFMS_SYSTEM_URI_PRIVATE is unset" && usage && exit 1
[ -z ${OWFMS_SYSTEM_URI_PUBLIC+x} ] && echo "OWFMS_SYSTEM_URI_PUBLIC is unset" && usage && exit 1
[ -z ${OWFMS_S3_SECRET+x} ] && echo "OWFMS_S3_SECRET is unset" && usage && exit 1
[ -z ${OWFMS_S3_KEY+x} ] && echo "OWFMS_S3_KEY is unset" && usage && exit 1
## OWProv configuration variables
[ -z ${OWPROV_SYSTEM_URI_PRIVATE+x} ] && echo "OWPROV_SYSTEM_URI_PRIVATE is unset" && usage && exit 1
[ -z ${OWPROV_SYSTEM_URI_PUBLIC+x} ] && echo "OWPROV_SYSTEM_URI_PUBLIC is unset" && usage && exit 1
## OWAnalytics configuration variables
[ -z ${OWANALYTICS_SYSTEM_URI_PRIVATE+x} ] && echo "OWANALYTICS_SYSTEM_URI_PRIVATE is unset" && usage && exit 1
[ -z ${OWANALYTICS_SYSTEM_URI_PUBLIC+x} ] && echo "OWANALYTICS_SYSTEM_URI_PUBLIC is unset" && usage && exit 1
## OWSub configuration variables
[ -z ${OWSUB_SYSTEM_URI_PRIVATE+x} ] && echo "OWSUB_SYSTEM_URI_PRIVATE is unset" && usage && exit 1
[ -z ${OWSUB_SYSTEM_URI_PUBLIC+x} ] && echo "OWSUB_SYSTEM_URI_PUBLIC is unset" && usage && exit 1
## cert related variables
[ -z ${WEBSOCKET_CERT+x} ] && echo "WEBSOCKET_CERT is unset" && usage && exit 1
[ -z ${WEBSOCKET_KEY+x} ] && echo "WEBSOCKET_KEY is unset" && usage && exit 1

# Clone repo and copy certificates
mkdir wlan-cloud-ucentral-deploy-tmp
git clone --branch $DEPLOY_VERSION https://github.com/Telecominfraproject/wlan-cloud-ucentral-deploy.git /wlan-cloud-ucentral-deploy-tmp 
mv -f /wlan-cloud-ucentral-deploy-tmp/* /wlan-cloud-ucentral-deploy/ && rm -r wlan-cloud-ucentral-deploy-tmp
cd wlan-cloud-ucentral-deploy/docker-compose

# Search and replace variable values in env files
sed -i "s~\(^INTERNAL_OWGW_HOSTNAME=\).*~\1$INTERNAL_OWGW_HOSTNAME~" .env
sed -i "s~\(^INTERNAL_OWSEC_HOSTNAME=\).*~\1$INTERNAL_OWSEC_HOSTNAME~" .env
sed -i "s~\(^INTERNAL_OWFMS_HOSTNAME=\).*~\1$INTERNAL_OWFMS_HOSTNAME~" .env
sed -i "s~\(^INTERNAL_OWPROV_HOSTNAME=\).*~\1$INTERNAL_OWPROV_HOSTNAME~" .env
sed -i "s~\(^INTERNAL_OWANALYTICS_HOSTNAME=\).*~\1$INTERNAL_OWANALYTICS_HOSTNAME~" .env
sed -i "s~\(^INTERNAL_OWSUB_HOSTNAME=\).*~\1$INTERNAL_OWSUB_HOSTNAME~" .env

sed -i "s~\(^FILEUPLOADER_HOST_NAME=\).*~\1$OWGW_FILEUPLOADER_HOST_NAME~" owgw.env
sed -i "s~\(^FILEUPLOADER_URI=\).*~\1$OWGW_FILEUPLOADER_URI~" owgw.env
sed -i "s~\(^SYSTEM_URI_PRIVATE=\).*~\1$OWGW_SYSTEM_URI_PRIVATE~" owgw.env
sed -i "s~\(^SYSTEM_URI_PUBLIC=\).*~\1$OWGW_SYSTEM_URI_PUBLIC~" owgw.env
sed -i "s~\(^SYSTEM_URI_UI=\).*~\1$SYSTEM_URI_UI~" owgw.env
sed -i "s~\(^RTTY_SERVER=\).*~\1$OWGW_RTTY_SERVER~" owgw.env

if [[ ! -z "$SIMULATORID" ]]; then
  sed -i "s~.*SIMULATORID=.*~SIMULATORID=$SIMULATORID~" owgw.env
fi

sed -i "s~\(^DEFAULT_UCENTRALSEC_URL=\).*~\1$DEFAULT_UCENTRALSEC_URL~" owgw-ui.env

sed -i "s~.*AUTHENTICATION_DEFAULT_USERNAME=.*~AUTHENTICATION_DEFAULT_USERNAME=$OWSEC_AUTHENTICATION_DEFAULT_USERNAME~" owsec.env
sed -i "s~.*AUTHENTICATION_DEFAULT_PASSWORD=.*~AUTHENTICATION_DEFAULT_PASSWORD=$OWSEC_AUTHENTICATION_DEFAULT_PASSWORD~" owsec.env
sed -i "s~\(^SYSTEM_URI_PRIVATE=\).*~\1$OWSEC_SYSTEM_URI_PRIVATE~" owsec.env
sed -i "s~\(^SYSTEM_URI_PUBLIC=\).*~\1$OWSEC_SYSTEM_URI_PUBLIC~" owsec.env
sed -i "s~\(^SYSTEM_URI_UI=\).*~\1$SYSTEM_URI_UI~" owsec.env

sed -i "s~\(^SYSTEM_URI_PRIVATE=\).*~\1$OWFMS_SYSTEM_URI_PRIVATE~" owfms.env
sed -i "s~\(^SYSTEM_URI_PUBLIC=\).*~\1$OWFMS_SYSTEM_URI_PUBLIC~" owfms.env
sed -i "s~\(^SYSTEM_URI_UI=\).*~\1$SYSTEM_URI_UI~" owfms.env
sed -i "s~\(^S3_SECRET=\).*~\1$OWFMS_S3_SECRET~" owfms.env
sed -i "s~\(^S3_KEY=\).*~\1$OWFMS_S3_KEY~" owfms.env

sed -i "s~\(^SYSTEM_URI_PRIVATE=\).*~\1$OWPROV_SYSTEM_URI_PRIVATE~" owprov.env
sed -i "s~\(^SYSTEM_URI_PUBLIC=\).*~\1$OWPROV_SYSTEM_URI_PUBLIC~" owprov.env
sed -i "s~\(^SYSTEM_URI_UI=\).*~\1$SYSTEM_URI_UI~" owprov.env

sed -i "s~\(^DEFAULT_UCENTRALSEC_URL=\).*~\1$DEFAULT_UCENTRALSEC_URL~" owprov-ui.env
sed -i "s~\(^REACT_APP_UCENTRALSEC_URL=\).*~\1$REACT_APP_UCENTRALSEC_URL~" owprov-ui.env

sed -i "s~\(^SYSTEM_URI_PRIVATE=\).*~\1$OWANALYTICS_SYSTEM_URI_PRIVATE~" owanalytics.env
sed -i "s~\(^SYSTEM_URI_PUBLIC=\).*~\1$OWANALYTICS_SYSTEM_URI_PUBLIC~" owanalytics.env
sed -i "s~\(^SYSTEM_URI_UI=\).*~\1$SYSTEM_URI_UI~" owanalytics.env

sed -i "s~\(^SYSTEM_URI_PRIVATE=\).*~\1$OWSUB_SYSTEM_URI_PRIVATE~" owsub.env
sed -i "s~\(^SYSTEM_URI_PUBLIC=\).*~\1$OWSUB_SYSTEM_URI_PUBLIC~" owsub.env
sed -i "s~\(^SYSTEM_URI_UI=\).*~\1$SYSTEM_URI_UI~" owsub.env

# Run the deployment and attach to logs
cat $WEBSOCKET_CERT > certs/websocket-cert.pem
cat $WEBSOCKET_KEY > certs/websocket-key.pem
exec docker-compose up --attach-dependencies
