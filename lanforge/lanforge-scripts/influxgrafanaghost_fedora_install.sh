#!/bin/bash
# This bash script installs Influx, Grafana, and Ghost on Fedora or CentOS.
# Run this script as a normal user with sudo access.
# You need to provide your username at the beginning of the script.
# There are a few fields you will need to enter when this installs Ghost, and you will be prompted by the script.
# Many scripts in this library are built around Influx, Grafana, and Ghost. Influx is a time series database,
# Grafana has dashboards which display the data stored in Influx,
# and Ghost is a blogging platform which creates an easy way for a user to view automated reports which are built using LANforge scripts
# Once a user uses this script, the user can use those features with the credentials for the system this script sets up.

# After running this script, Grafana is at port 3000, Influx is at port 8086, and Ghost is at port 2368
# The user will need to login to those through a web browser to create login credentials, and find API tokens.
# These API tokens are needed to run many scripts in LANforge scripts with these three programs.

echo Type in your username here
read -r USER

#Influx installation
wget https://dl.influxdata.com/influxdb/releases/influxdb2-2.0.4.x86_64.rpm
sudo yum localinstall influxdb2-2.0.4.x86_64.rpm
sudo service influxdb start
sudo service influxdb enable

#Grafana installation
wget https://dl.grafana.com/oss/release/grafana-7.5.3-1.x86_64.rpm
sudo yum localinstall grafana-7.5.3-1.x86_64.rpm -y
sudo systemctl start grafana-server
sudo systemctl enable grafana-server

#Ghost installation
sudo adduser ghost
sudo usermod -aG sudo ghost
sudo ufw allow 'Nginx Full'
curl -sL https://deb.nodesource.com/setup_14.x | sudo -E bash
sudo npm install ghost-cli@latest -g
# Ensure that NPM is up to date
npm cache verify
sudo npm install -g n
sudo n stable
curl -sL https://deb.nodesource.com/setup_14.x | sudo -E bash
npm install ghost-cli@latest -g
sudo mkdir -p /var/www/ghostsite
sudo chown ${USER}:${USER} /var/www/ghostsite
sudo chmod 775 /var/www/ghostsite
cd /var/www/ghostsite
ghost install local