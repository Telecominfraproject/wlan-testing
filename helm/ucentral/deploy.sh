#!/bin/bash
set -e

# Usage function
usage () {
  echo;
  echo "This script is indended for OpenWIFI Cloud SDK deployment to TIP QA/Dev environments using assembly Helm chart (https://github.com/Telecominfraproject/wlan-cloud-ucentral-deploy/tree/main/chart) with configuration through environment variables";
  echo;
  echo "Required environment variables:"
  echo;
  echo "- NAMESPACE - namespace suffix that will used added for the Kubernetes environment (i.e. if you pass 'test', kubernetes namespace will be named 'ucentral-test')";
  echo "- DEPLOY_METHOD - deployment method for the chart deployment (supported methods - 'git' (will use helm-git from assembly chart) and 'bundle' (will use chart stored in the Artifactory0";
  echo "- CHART_VERSION - version of chart to be deployed from assembly chart (for 'git' method git ref may be passed, for 'bundle' method version of chart may be passed)";
  echo;
  echo "- VALUES_FILE_LOCATION - path to file with override values that may be used for deployment";
  echo "- OWGW_AUTH_USERNAME - username to be used for requests to OpenWIFI Security";
  echo "- OWGW_AUTH_PASSWORD - hashed password for OpenWIFI Security (details on this may be found in https://github.com/Telecominfraproject/wlan-cloud-ucentralsec/#authenticationdefaultpassword)";
  echo "- OWFMS_S3_SECRET - secret key that is used for OpenWIFI Firmware access to firmwares S3 bucket";
  echo "- OWFMS_S3_KEY - access key that is used for OpenWIFI Firmware access to firmwares S3 bucket";
  echo "- OWSEC_NEW_PASSWORD - password that should be set to default user instead of default password from properties";
  echo "- CERT_LOCATION - path to certificate in PEM format that will be used for securing all endpoint in all services";
  echo "- KEY_LOCATION - path to private key in PEM format that will be used for securing all endpoint in all services";
  echo;
  echo "Following environmnet variables may be passed, but will be ignored if CHART_VERSION is set to release (i.e. v2.4.0):"
  echo;
  echo "- OWGW_VERSION - OpenWIFI Gateway version to deploy (will be used for Docker image tag and git branch for Helm chart if git deployment is required)";
  echo "- OWGWUI_VERSION - OpenWIFI Web UI version to deploy (will be used for Docker image tag and git branch for Helm chart if git deployment is required)";
  echo "- OWSEC_VERSION - OpenWIFI Security version to deploy (will be used for Docker image tag and git branch for Helm chart if git deployment is required)";
  echo "- OWFMS_VERSION - OpenWIFI Firmware version to deploy (will be used for Docker image tag and git branch for Helm chart if git deployment is required)";
  echo "- OWPROV_VERSION - OpenWIFI Provisioning version to deploy (will be used for Docker image tag and git branch for Helm chart if git deployment is required)";
  echo "- OWPROVUI_VERSION - OpenWIFI Provisioning Web UI version to deploy (will be used for Docker image tag and git branch for Helm chart if git deployment is required)";
  echo "- OWANALYTICS_VERSION - OpenWIFI Analytics version to deploy (will be used for Docker image tag and git branch for Helm chart if git deployment is required)";
  echo "- OWSUB_VERSION - OpenWIFI Subscription (Userportal) version to deploy (will be used for Docker image tag and git branch for Helm chart if git deployment is required)";
  echo;
  echo "Optional environment variables:"
  echo;
  echo "- EXTRA_VALUES - extra values that should be passed to Helm deployment separated by comma (,)"
  echo "- DEVICE_CERT_LOCATION - path to certificate in PEM format that will be used for load simulator";
  echo "- DEVICE_KEY_LOCATION - path to private key in PEM format that will be used for load simulator";
  echo "- USE_SEPARATE_OWGW_LB - flag that should change split external DNS for OWGW and other services"
}

# Global variables
VALUES_FILE_LOCATION_SPLITTED=()
EXTRA_VALUES_SPLITTED=()

# Helper functions
check_if_chart_version_is_release() {
  PARSED_CHART_VERSION=$(echo $CHART_VERSION | grep -xP "v\d+\.\d+\.\d+.*")
  if [[ -z "$PARSED_CHART_VERSION" ]]; then
    return 1
  else
    return 0
  fi
}

# Check if required environment variables were passed
## Deployment specifics
[ -z ${DEPLOY_METHOD+x} ] && echo "DEPLOY_METHOD is unset" && usage && exit 1
[ -z ${CHART_VERSION+x} ] && echo "CHART_VERSION is unset" && usage && exit 1
if check_if_chart_version_is_release; then
  echo "Chart version ($CHART_VERSION) is release version, ignoring services versions"
else
  echo "Chart version ($CHART_VERSION) is not release version, checking if services versions are set"
  [ -z ${OWGW_VERSION+x} ] && echo "OWGW_VERSION is unset" && usage && exit 1
  [ -z ${OWGWUI_VERSION+x} ] && echo "OWGWUI_VERSION is unset" && usage && exit 1
  [ -z ${OWSEC_VERSION+x} ] && echo "OWSEC_VERSION is unset" && usage && exit 1
  [ -z ${OWFMS_VERSION+x} ] && echo "OWFMS_VERSION is unset" && usage && exit 1
  [ -z ${OWPROV_VERSION+x} ] && echo "OWPROV_VERSION is unset" && usage && exit 1
  [ -z ${OWPROVUI_VERSION+x} ] && echo "OWPROVUI_VERSION is unset" && usage && exit 1
  [ -z ${OWANALYTICS_VERSION+x} ] && echo "OWANALYTICS_VERSION is unset" && usage && exit 1
  [ -z ${OWSUB_VERSION+x} ] && echo "OWSUB_VERSION is unset" && usage && exit 1
fi
## Environment specifics
[ -z ${NAMESPACE+x} ] && echo "NAMESPACE is unset" && usage && exit 1
## Variables specifics
[ -z ${VALUES_FILE_LOCATION+x} ] && echo "VALUES_FILE_LOCATION is unset" && usage && exit 1
[ -z ${OWGW_AUTH_USERNAME+x} ] && echo "OWGW_AUTH_USERNAME is unset" && usage && exit 1
[ -z ${OWGW_AUTH_PASSWORD+x} ] && echo "OWGW_AUTH_PASSWORD is unset" && usage && exit 1
[ -z ${OWFMS_S3_SECRET+x} ] && echo "OWFMS_S3_SECRET is unset" && usage && exit 1
[ -z ${OWFMS_S3_KEY+x} ] && echo "OWFMS_S3_KEY is unset" && usage && exit 1
[ -z ${OWSEC_NEW_PASSWORD+x} ] && echo "OWSEC_NEW_PASSWORD is unset" && usage && exit 1
[ -z ${CERT_LOCATION+x} ] && echo "CERT_LOCATION is unset" && usage && exit 1
[ -z ${KEY_LOCATION+x} ] && echo "KEY_LOCATION is unset" && usage && exit 1

[ -z ${DEVICE_CERT_LOCATION+x} ] && echo "DEVICE_CERT_LOCATION is unset, setting it to CERT_LOCATION" && export DEVICE_CERT_LOCATION=$CERT_LOCATION
[ -z ${DEVICE_KEY_LOCATION+x} ] && echo "DEVICE_KEY_LOCATION is unset, setting it to KEY_LOCATION" && export DEVICE_KEY_LOCATION=$KEY_LOCATION

# Transform some environment variables
export OWGW_VERSION_TAG=$(echo ${OWGW_VERSION} | tr '/' '-')
export OWGWUI_VERSION_TAG=$(echo ${OWGWUI_VERSION} | tr '/' '-')
export OWSEC_VERSION_TAG=$(echo ${OWSEC_VERSION} | tr '/' '-')
export OWFMS_VERSION_TAG=$(echo ${OWFMS_VERSION} | tr '/' '-')
export OWPROV_VERSION_TAG=$(echo ${OWPROV_VERSION} | tr '/' '-')
export OWPROVUI_VERSION_TAG=$(echo ${OWPROVUI_VERSION} | tr '/' '-')
export OWANALYTICS_VERSION_TAG=$(echo ${OWANALYTICS_VERSION} | tr '/' '-')
export OWSUB_VERSION_TAG=$(echo ${OWSUB_VERSION} | tr '/' '-')

# Debug get bash version
bash --version > /dev/stderr

# Check deployment method that's required for this environment
helm plugin install https://github.com/databus23/helm-diff || true
if [[ "$DEPLOY_METHOD" == "git" ]]; then
  helm plugin install https://github.com/aslafy-z/helm-git --version 0.10.0 || true
  rm -rf wlan-cloud-ucentral-deploy || true
  git clone https://github.com/Telecominfraproject/wlan-cloud-ucentral-deploy.git
  cd wlan-cloud-ucentral-deploy
  git checkout $CHART_VERSION
  cd chart
  if ! check_if_chart_version_is_release; then
    sed -i '/wlan-cloud-ucentralgw@/s/ref=.*/ref='${OWGW_VERSION}'\"/g' Chart.yaml
    sed -i '/wlan-cloud-ucentralgw-ui@/s/ref=.*/ref='${OWGWUI_VERSION}'\"/g' Chart.yaml
    sed -i '/wlan-cloud-ucentralsec@/s/ref=.*/ref='${OWSEC_VERSION}'\"/g' Chart.yaml
    sed -i '/wlan-cloud-ucentralfms@/s/ref=.*/ref='${OWFMS_VERSION}'\"/g' Chart.yaml
    sed -i '/wlan-cloud-owprov@/s/ref=.*/ref='${OWPROV_VERSION}'\"/g' Chart.yaml
    sed -i '/wlan-cloud-owprov-ui@/s/ref=.*/ref='${OWPROVUI_VERSION}'\"/g' Chart.yaml
    sed -i '/wlan-cloud-analytics@/s/ref=.*/ref='${OWANALYTICS_VERSION}'\"/g' Chart.yaml
    sed -i '/wlan-cloud-userportal@/s/ref=.*/ref='${OWSUB_VERSION}'\"/g' Chart.yaml
  fi
  helm repo add bitnami https://charts.bitnami.com/bitnami
  helm repo update
  helm dependency update
  cd ../..
  export DEPLOY_SOURCE="wlan-cloud-ucentral-deploy/chart"
else
  if [[ "$DEPLOY_METHOD" == "bundle" ]]; then
    helm repo add tip-wlan-cloud-ucentral-helm https://tip.jfrog.io/artifactory/tip-wlan-cloud-ucentral-helm/ || true
    export DEPLOY_SOURCE="tip-wlan-cloud-ucentral-helm/openwifi --version $CHART_VERSION"
  else
    echo "Deploy method is not correct: $DEPLOY_METHOD. Valid value - git or bundle"
    exit 1
  fi
fi

VALUES_FILES_FLAGS=()
IFS=',' read -ra VALUES_FILE_LOCATION_SPLITTED <<< "$VALUES_FILE_LOCATION"
for VALUE_FILE in ${VALUES_FILE_LOCATION_SPLITTED[*]}; do
  VALUES_FILES_FLAGS+=("-f" $VALUE_FILE)
done
EXTRA_VALUES_FLAGS=()
IFS=',' read -ra EXTRA_VALUES_SPLITTED <<< "$EXTRA_VALUES"
for EXTRA_VALUE in ${EXTRA_VALUES_SPLITTED[*]}; do
  EXTRA_VALUES_FLAGS+=("--set" $EXTRA_VALUE)
done

if [[ "$USE_SEPARATE_OWGW_LB" == "true" ]]; then
  export HAPROXY_SERVICE_DNS_RECORDS="sec-${NAMESPACE}.cicd.lab.wlan.tip.build\,fms-${NAMESPACE}.cicd.lab.wlan.tip.build\,prov-${NAMESPACE}.cicd.lab.wlan.tip.build\,analytics-${NAMESPACE}.cicd.lab.wlan.tip.build\,sub-${NAMESPACE}.cicd.lab.wlan.tip.build"
  export OWGW_SERVICE_DNS_RECORDS="gw-${NAMESPACE}.cicd.lab.wlan.tip.build"
else
  export HAPROXY_SERVICE_DNS_RECORDS="gw-${NAMESPACE}.cicd.lab.wlan.tip.build\,sec-${NAMESPACE}.cicd.lab.wlan.tip.build\,fms-${NAMESPACE}.cicd.lab.wlan.tip.build\,prov-${NAMESPACE}.cicd.lab.wlan.tip.build\,analytics-${NAMESPACE}.cicd.lab.wlan.tip.build\,sub-${NAMESPACE}.cicd.lab.wlan.tip.build"
  export OWGW_SERVICE_DNS_RECORDS=""
fi

# Run the deployment
helm upgrade --install --create-namespace --wait --timeout 60m \
  --namespace openwifi-${NAMESPACE} \
  ${VALUES_FILES_FLAGS[*]} \
  --set owgw.services.owgw.annotations."external-dns\.alpha\.kubernetes\.io/hostname"=gw-${NAMESPACE}.cicd.lab.wlan.tip.build \
  --set owgw.configProperties."openwifi\.fileuploader\.host\.0\.name"=gw-${NAMESPACE}.cicd.lab.wlan.tip.build \
  --set owgw.configProperties."rtty\.server"=gw-${NAMESPACE}.cicd.lab.wlan.tip.build \
  --set owgw.configProperties."openwifi\.system\.uri\.public"=https://gw-${NAMESPACE}.cicd.lab.wlan.tip.build:16002 \
  --set owgw.configProperties."openwifi\.system\.uri\.private"=https://owgw-owgw:17002 \
  --set owgw.configProperties."openwifi\.system\.uri\.ui"=https://webui-${NAMESPACE}.cicd.lab.wlan.tip.build \
  --set owgw.public_env_variables.OWSEC=sec-${NAMESPACE}.cicd.lab.wlan.tip.build:16001 \
  --set owsec.configProperties."authentication\.default\.username"=${OWGW_AUTH_USERNAME} \
  --set owsec.configProperties."authentication\.default\.password"=${OWGW_AUTH_PASSWORD} \
  --set owsec.services.owsec.annotations."external-dns\.alpha\.kubernetes\.io/hostname"=sec-${NAMESPACE}.cicd.lab.wlan.tip.build \
  --set owsec.configProperties."openwifi\.system\.uri\.public"=https://sec-${NAMESPACE}.cicd.lab.wlan.tip.build:16001 \
  --set owsec.configProperties."openwifi\.system\.uri\.private"=https://owsec-owsec:17001 \
  --set owsec.configProperties."openwifi\.system\.uri\.ui"=https://webui-${NAMESPACE}.cicd.lab.wlan.tip.build \
  --set owfms.configProperties."s3\.secret"=${OWFMS_S3_SECRET} \
  --set owfms.configProperties."s3\.key"=${OWFMS_S3_KEY} \
  --set owfms.services.owfms.annotations."external-dns\.alpha\.kubernetes\.io/hostname"=fms-${NAMESPACE}.cicd.lab.wlan.tip.build \
  --set owfms.configProperties."openwifi\.system\.uri\.public"=https://fms-${NAMESPACE}.cicd.lab.wlan.tip.build:16004 \
  --set owfms.configProperties."openwifi\.system\.uri\.private"=https://owfms-owfms:17004 \
  --set owfms.configProperties."openwifi\.system\.uri\.ui"=https://webui-${NAMESPACE}.cicd.lab.wlan.tip.build \
  --set owfms.public_env_variables.OWSEC=sec-${NAMESPACE}.cicd.lab.wlan.tip.build:16001 \
  --set owgwui.ingresses.default.annotations."external-dns\.alpha\.kubernetes\.io/hostname"=webui-${NAMESPACE}.cicd.lab.wlan.tip.build \
  --set owgwui.ingresses.default.hosts={webui-${NAMESPACE}.cicd.lab.wlan.tip.build} \
  --set owgwui.public_env_variables.DEFAULT_UCENTRALSEC_URL=https://sec-${NAMESPACE}.cicd.lab.wlan.tip.build:16001 \
  --set owprov.services.owprov.annotations."external-dns\.alpha\.kubernetes\.io/hostname"=prov-${NAMESPACE}.cicd.lab.wlan.tip.build \
  --set owprov.configProperties."openwifi\.system\.uri\.public"=https://prov-${NAMESPACE}.cicd.lab.wlan.tip.build:16005 \
  --set owprov.configProperties."openwifi\.system\.uri\.private"=https://owprov-owprov:17005 \
  --set owprov.configProperties."openwifi\.system\.uri\.ui"=https://webui-${NAMESPACE}.cicd.lab.wlan.tip.build \
  --set owprov.public_env_variables.OWSEC=sec-${NAMESPACE}.cicd.lab.wlan.tip.build:16001 \
  --set owprovui.ingresses.default.annotations."external-dns\.alpha\.kubernetes\.io/hostname"=provui-${NAMESPACE}.cicd.lab.wlan.tip.build \
  --set owprovui.ingresses.default.hosts={provui-${NAMESPACE}.cicd.lab.wlan.tip.build} \
  --set owprovui.public_env_variables.DEFAULT_UCENTRALSEC_URL=https://sec-${NAMESPACE}.cicd.lab.wlan.tip.build:16001 \
  --set owprovui.public_env_variables.REACT_APP_UCENTRALSEC_URL=https://sec-${NAMESPACE}.cicd.lab.wlan.tip.build:16001 \
  --set owanalytics.services.owanalytics.annotations."external-dns\.alpha\.kubernetes\.io/hostname"=analytics-${NAMESPACE}.cicd.lab.wlan.tip.build \
  --set owanalytics.configProperties."openwifi\.system\.uri\.public"=https://analytics-${NAMESPACE}.cicd.lab.wlan.tip.build:16009 \
  --set owanalytics.configProperties."openwifi\.system\.uri\.private"=https://owanalytics-owanalytics:17009 \
  --set owanalytics.configProperties."openwifi\.system\.uri\.ui"=https://webui-${NAMESPACE}.cicd.lab.wlan.tip.build \
  --set owanalytics.public_env_variables.OWSEC=sec-${NAMESPACE}.cicd.lab.wlan.tip.build:16001 \
  --set owsub.services.owsub.annotations."external-dns\.alpha\.kubernetes\.io/hostname"=sub-${NAMESPACE}.cicd.lab.wlan.tip.build \
  --set owsub.configProperties."openwifi\.system\.uri\.public"=https://sub-${NAMESPACE}.cicd.lab.wlan.tip.build:16006 \
  --set owsub.configProperties."openwifi\.system\.uri\.private"=https://owsub-owsub:17006 \
  --set owsub.configProperties."openwifi\.system\.uri\.ui"=https://webui-${NAMESPACE}.cicd.lab.wlan.tip.build \
  --set owsub.public_env_variables.OWSEC=sec-${NAMESPACE}.cicd.lab.wlan.tip.build:16001 \
  --set clustersysteminfo.public_env_variables.OWSEC=sec-${NAMESPACE}.cicd.lab.wlan.tip.build:16001 \
  --set clustersysteminfo.secret_env_variables.OWSEC_NEW_PASSWORD=${OWSEC_NEW_PASSWORD} \
  --set owls.services.owls.annotations."external-dns\.alpha\.kubernetes\.io/hostname"=ls-${NAMESPACE}.cicd.lab.wlan.tip.build \
  --set owls.configProperties."openwifi\.system\.uri\.public"=https://ls-${NAMESPACE}.cicd.lab.wlan.tip.build:16007 \
  --set owls.configProperties."openwifi\.system\.uri\.private"=https://owls-owls:17007 \
  --set owls.configProperties."openwifi\.system\.uri\.ui"=https://webui-${NAMESPACE}.cicd.lab.wlan.tip.build \
  --set owlsui.ingresses.default.annotations."external-dns\.alpha\.kubernetes\.io/hostname"=lsui-${NAMESPACE}.cicd.lab.wlan.tip.build \
  --set owlsui.ingresses.default.hosts={lsui-${NAMESPACE}.cicd.lab.wlan.tip.build} \
  --set owlsui.public_env_variables.DEFAULT_UCENTRALSEC_URL=https://sec-${NAMESPACE}.cicd.lab.wlan.tip.build:16001 \
  --set haproxy.service.annotations."external-dns\.alpha\.kubernetes\.io/hostname"=$HAPROXY_SERVICE_DNS_RECORDS \
  --set owgw.services.owgw.annotations."external-dns\.alpha\.kubernetes\.io/hostname"=$OWGW_SERVICE_DNS_RECORDS \
  ${EXTRA_VALUES_FLAGS[*]} \
  --set-file owgw.certs."restapi-cert\.pem"=$CERT_LOCATION \
  --set-file owgw.certs."restapi-key\.pem"=$KEY_LOCATION \
  --set-file owgw.certs."websocket-cert\.pem"=$CERT_LOCATION \
  --set-file owgw.certs."websocket-key\.pem"=$KEY_LOCATION \
  --set-file owsec.certs."restapi-cert\.pem"=$CERT_LOCATION \
  --set-file owsec.certs."restapi-key\.pem"=$KEY_LOCATION \
  --set-file owfms.certs."restapi-cert\.pem"=$CERT_LOCATION \
  --set-file owfms.certs."restapi-key\.pem"=$KEY_LOCATION \
  --set-file owprov.certs."restapi-cert\.pem"=$CERT_LOCATION \
  --set-file owprov.certs."restapi-key\.pem"=$KEY_LOCATION \
  --set-file owls.certs."restapi-cert\.pem"=$CERT_LOCATION \
  --set-file owls.certs."restapi-key\.pem"=$KEY_LOCATION \
  --set-file owls.certs."device-cert\.pem"=$DEVICE_CERT_LOCATION \
  --set-file owls.certs."device-key\.pem"=$DEVICE_KEY_LOCATION \
  --set-file owanalytics.certs."restapi-cert\.pem"=$CERT_LOCATION \
  --set-file owanalytics.certs."restapi-key\.pem"=$KEY_LOCATION \
  --set-file owsub.certs."restapi-cert\.pem"=$CERT_LOCATION \
  --set-file owsub.certs."restapi-key\.pem"=$KEY_LOCATION \
  tip-openwifi $DEPLOY_SOURCE
