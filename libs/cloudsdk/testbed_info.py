"""
    A set of constants describing cloud controllers properties
"""
import os

SDK_BASE_URLS = {
    "nola-01": "https://wlan-portal-svc-nola-01.cicd.lab.wlan.tip.build",
    "nola-02": "https://wlan-portal-svc-nola-02.cicd.lab.wlan.tip.build",
    "nola-04": "https://wlan-portal-svc-nola-04.cicd.lab.wlan.tip.build",
    "nola-ext-03": "https://wlan-portal-svc-nola-ext-03.cicd.lab.wlan.tip.build",
    "nola-ext-04": "https://wlan-portal-svc-nola-ext-04.cicd.lab.wlan.tip.build",
    "nola-ext-05": "https://wlan-portal-svc-nola-ext-05.cicd.lab.wlan.tip.build"
}

LOGIN_CREDENTIALS = {
    "userId": "support@example.com",
    "password": "support"
}

JFROG_CREDENTIALS = {
    "userId": os.getenv('JFROG_USER'),
    "password": os.getenv('JFROG_PWD')
}