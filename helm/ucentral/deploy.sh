#!/bin/bash
set -e

# Usage function
usage () {
  echo;
  echo "This script is indended for uCentral Cloud SDK deployment to TIP QA/Dev environments using assembly Helm chart (https://github.com/Telecominfraproject/wlan-cloud-ucentral-deploy/tree/main/chart) with configuration through environment variables";
  echo;
  echo "Required environment variables:"
  echo;
  echo "- NAMESPACE - namespace suffix that will used added for the Kubernetes environment (i.e. if you pass 'test', kubernetes namespace will be named 'ucentral-test')";
  echo "- UCENTRALGW_VERSION - uCentralGW version to deploy (will be used for Docker image tag and git branch for Helm chart if git deployment is required)";
  echo "- UCENTRALGWUI_VERSION - uCentralGW UI version to deploy (will be used for Docker image tag and git branch for Helm chart if git deployment is required)";
  echo "- UCENTRALSEC_VERSION - uCentralSec version to deploy (will be used for Docker image tag and git branch for Helm chart if git deployment is required)";
  echo "- UCENTRALFMS_VERSION - uCentralFMS version to deploy (will be used for Docker image tag and git branch for Helm chart if git deployment is required)";
  echo;
  echo "- DEPLOY_METHOD - deployment method for the chart deployment (supported methods - 'git' (will use helm-git from assembly chart) and 'bundle' (will use chart stored in the Artifactory0";
  echo "- CHART_VERSION - version of chart to be deployed from assembly chart (for 'git' method git ref may be passed, for 'bundle' method version of chart may be passed)";
  echo;
  echo "- VALUES_FILE_LOCATION - path to file with override values that may be used for deployment";
  echo "- RTTY_TOKEN - token to be used for rttys and uCentralGW for remote tty sessions";
  echo "- UCENTRALGW_AUTH_USERNAME - username to be used for requests to uCentralSec";
  echo "- UCENTRALGW_AUTH_PASSWORD - hashed password for uCentralSec (details on this may be found in https://github.com/Telecominfraproject/wlan-cloud-ucentralsec/#authenticationdefaultpassword)";
  echo "- UCENTRALFMS_S3_SECRET - secret key that is used for uCentralFMS access to firmwares S3 bucket";
  echo "- UCENTRALFMS_S3_KEY - access key that is used for uCentralFMS access to firmwares S3 bucket";
  echo "- CERT_LOCATION - path to certificate in PEM format that will be used for securing all endpoint in all services";
  echo "- KEY_LOCATION - path to private key in PEM format that will be used for securing all endpoint in all services";
}

# Check if required environment variables were passed
## Environment specifics
[ -z ${NAMESPACE+x} ] && echo "NAMESPACE is unset" && usage && exit 1
[ -z ${UCENTRALGW_VERSION+x} ] && echo "UCENTRALGW_VERSION is unset" && usage && exit 1
[ -z ${UCENTRALGWUI_VERSION+x} ] && echo "UCENTRALGWUI_VERSION is unset" && usage && exit 1
[ -z ${UCENTRALSEC_VERSION+x} ] && echo "UCENTRALSEC_VERSION is unset" && usage && exit 1
[ -z ${UCENTRALFMS_VERSION+x} ] && echo "UCENTRALFMS_VERSION is unset" && usage && exit 1
## Deployment specifics
[ -z ${DEPLOY_METHOD+x} ] && echo "DEPLOY_METHOD is unset" && usage && exit 1
[ -z ${CHART_VERSION+x} ] && echo "CHART_VERSION is unset" && usage && exit 1
## Variables specifics
[ -z ${VALUES_FILE_LOCATION+x} ] && echo "VALUES_FILE_LOCATION is unset" && usage && exit 1
[ -z ${RTTY_TOKEN+x} ] && echo "RTTY_TOKEN is unset" && usage && exit 1
[ -z ${UCENTRALGW_AUTH_USERNAME+x} ] && echo "UCENTRALGW_AUTH_USERNAME is unset" && usage && exit 1
[ -z ${UCENTRALGW_AUTH_PASSWORD+x} ] && echo "UCENTRALGW_AUTH_PASSWORD is unset" && usage && exit 1
[ -z ${UCENTRALFMS_S3_SECRET+x} ] && echo "UCENTRALFMS_S3_SECRET is unset" && usage && exit 1
[ -z ${UCENTRALFMS_S3_KEY+x} ] && echo "UCENTRALFMS_S3_KEY is unset" && usage && exit 1
[ -z ${CERT_LOCATION+x} ] && echo "CERT_LOCATION is unset" && usage && exit 1
[ -z ${KEY_LOCATION+x} ] && echo "KEY_LOCATION is unset" && usage && exit 1

# Transform some environment variables
export UCENTRALGW_VERSION_TAG=$(echo ${UCENTRALGW_VERSION} | tr '/' '-')
export UCENTRALGWUI_VERSION_TAG=$(echo ${UCENTRALGWUI_VERSION} | tr '/' '-')
export UCENTRALSEC_VERSION_TAG=$(echo ${UCENTRALSEC_VERSION} | tr '/' '-')
export UCENTRALFMS_VERSION_TAG=$(echo ${UCENTRALFMS_VERSION} | tr '/' '-')

# Check deployment method that's required for this environment
helm plugin install https://github.com/databus23/helm-diff || true
if [[ "$DEPLOY_METHOD" == "git" ]]; then
  helm plugin install https://github.com/aslafy-z/helm-git --version 0.10.0 || true
  rm -rf wlan-cloud-ucentral-deploy || true
  git clone https://github.com/Telecominfraproject/wlan-cloud-ucentral-deploy.git
  cd wlan-cloud-ucentral-deploy
  git checkout $CHART_VERSION
  cd chart
  sed -i '/wlan-cloud-ucentralgw@/s/ref=.*/ref='${UCENTRALGW_VERSION}'\"/g' Chart.yaml
  sed -i '/wlan-cloud-ucentralgw-ui@/s/ref=.*/ref='${UCENTRALGWUI_VERSION}'\"/g' Chart.yaml
  sed -i '/wlan-cloud-ucentralsec@/s/ref=.*/ref='${UCENTRALSEC_VERSION}'\"/g' Chart.yaml
  sed -i '/wlan-cloud-ucentralfms@/s/ref=.*/ref='${UCENTRALFMS_VERSION}'\"/g' Chart.yaml
  helm repo add bitnami https://charts.bitnami.com/bitnami
  helm repo update
  helm dependency update
  cd ../..
  export DEPLOY_SOURCE="wlan-cloud-ucentral-deploy/chart"
else
  if [[ "$DEPLOY_METHOD" == "bundle" ]]; then
    helm repo add tip-wlan-cloud-ucentral-helm https://tip.jfrog.io/artifactory/tip-wlan-cloud-ucentral-helm/ || true
    export DEPLOY_SOURCE="tip-wlan-cloud-ucentral-helm/wlan-cloud-ucentral --version $CHART_VERSION"
  else
    echo "Deploy method is not correct: $DEPLOY_METHOD. Valid value - git or bundle"
    exit 1
  fi
fi

# Run the deployment
helm upgrade --install --create-namespace --wait --timeout 20m \
  --namespace ucentral-${NAMESPACE} \
  -f $VALUES_FILE_LOCATION \
  --set ucentralgw.configProperties."rtty\.token"=${RTTY_TOKEN} \
  --set ucentralsec.configProperties."authentication\.default\.username"=${UCENTRALGW_AUTH_USERNAME} \
  --set ucentralsec.configProperties."authentication\.default\.password"=${UCENTRALGW_AUTH_PASSWORD} \
  --set rttys.config.token=${RTTY_TOKEN} \
  --set ucentralfms.configProperties."s3\.secret"=${UCENTRALFMS_S3_SECRET} \
  --set ucentralfms.configProperties."s3\.key"=${UCENTRALFMS_S3_KEY} \
  --set ucentralgw.services.ucentralgw.annotations."external-dns\.alpha\.kubernetes\.io/hostname"=gw-ucentral-${NAMESPACE}.cicd.lab.wlan.tip.build \
  --set ucentralgw.configProperties."ucentral\.fileuploader\.host\.0\.name"=gw-ucentral-${NAMESPACE}.cicd.lab.wlan.tip.build \
  --set ucentralgw.configProperties."rtty\.server"=rtty-ucentral-${NAMESPACE}.cicd.lab.wlan.tip.build \
  --set ucentralgw.configProperties."ucentral\.system\.uri\.public"=https://gw-ucentral-${NAMESPACE}.cicd.lab.wlan.tip.build:16002 \
  --set ucentralgw.configProperties."ucentral\.system\.uri\.private"=https://gw-ucentral-${NAMESPACE}.cicd.lab.wlan.tip.build:17002 \
  --set ucentralgw.configProperties."ucentral\.system\.uri\.ui"=https://webui-ucentral-${NAMESPACE}.cicd.lab.wlan.tip.build \
  --set ucentralsec.services.ucentralsec.annotations."external-dns\.alpha\.kubernetes\.io/hostname"=sec-ucentral-${NAMESPACE}.cicd.lab.wlan.tip.build \
  --set ucentralsec.configProperties."ucentral\.system\.uri\.public"=https://sec-ucentral-${NAMESPACE}.cicd.lab.wlan.tip.build:16001 \
  --set ucentralsec.configProperties."ucentral\.system\.uri\.private"=https://sec-ucentral-${NAMESPACE}.cicd.lab.wlan.tip.build:17001 \
  --set ucentralsec.configProperties."ucentral\.system\.uri\.ui"=https://webui-ucentral-${NAMESPACE}.cicd.lab.wlan.tip.build \
  --set rttys.services.rttys.annotations."external-dns\.alpha\.kubernetes\.io/hostname"=rtty-ucentral-${NAMESPACE}.cicd.lab.wlan.tip.build \
  --set ucentralgwui.ingresses.default.annotations."external-dns\.alpha\.kubernetes\.io/hostname"=webui-ucentral-${NAMESPACE}.cicd.lab.wlan.tip.build \
  --set ucentralgwui.ingresses.default.hosts={webui-ucentral-${NAMESPACE}.cicd.lab.wlan.tip.build} \
  --set ucentralgwui.public_env_variables.DEFAULT_UCENTRALSEC_URL=https://sec-ucentral-${NAMESPACE}.cicd.lab.wlan.tip.build:16001 \
  --set ucentralfms.services.ucentralfms.annotations."external-dns\.alpha\.kubernetes\.io/hostname"=fms-ucentral-${NAMESPACE}.cicd.lab.wlan.tip.build \
  --set ucentralfms.configProperties."ucentral\.system\.uri\.public"=https://fms-ucentral-${NAMESPACE}.cicd.lab.wlan.tip.build:16004 \
  --set ucentralfms.configProperties."ucentral\.system\.uri\.private"=https://fms-ucentral-${NAMESPACE}.cicd.lab.wlan.tip.build:17004 \
  --set ucentralfms.configProperties."ucentral\.system\.uri\.ui"=https://webui-ucentral-${NAMESPACE}.cicd.lab.wlan.tip.build \
  --set-file ucentralgw.certs."restapi-cert\.pem"=$CERT_LOCATION \
  --set-file ucentralgw.certs."restapi-key\.pem"=$KEY_LOCATION \
  --set-file ucentralgw.certs."websocket-cert\.pem"=$CERT_LOCATION \
  --set-file ucentralgw.certs."websocket-key\.pem"=$KEY_LOCATION \
  --set-file rttys.certs."restapi-cert\.pem"=$CERT_LOCATION \
  --set-file rttys.certs."restapi-key\.pem"=$KEY_LOCATION \
  --set-file ucentralsec.certs."restapi-cert\.pem"=$CERT_LOCATION \
  --set-file ucentralsec.certs."restapi-key\.pem"=$KEY_LOCATION \
  --set-file ucentralfms.certs."restapi-cert\.pem"=$CERT_LOCATION \
  --set-file ucentralfms.certs."restapi-key\.pem"=$KEY_LOCATION \
  --set ucentralgw.images.ucentralgw.tag=$UCENTRALGW_VERSION_TAG \
  --set ucentralgwui.images.ucentralgwui.tag=$UCENTRALGWUI_VERSION_TAG \
  --set ucentralsec.images.ucentralsec.tag=$UCENTRALSEC_VERSION_TAG \
  --set ucentralfms.images.ucentralfms.tag=$UCENTRALFMS_VERSION_TAG \
  tip-ucentral $DEPLOY_SOURCE
