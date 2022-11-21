#!/bin/bash
#This script installs Influx, Grafana, and Ghost on Ubuntu.
#Run this script as a normal user with sudo access.
#You need to provide your username at the beginning of the script.
#There are a few fields you will need to enter when it is installing Ghost, and you will be prompted by the script.
#Lanforge scripts is built around Influx, Grafana, and Ghost. Influx is a time series database,
#Grafana has dashboards which display the data stored in Influx,
#and Ghost is a blogging platform which creates an easy way for a user to view automated reports which are built using LANforge scripts
#Once a user uses this script, the user can use those features with the credentials for the system this script sets up.

#After running this script, Grafana is accessible through port 3000, Influx is at port 8086, and Ghost is accessible at 2368
#The user will need to login to those through a web browser to create login credentials, and find API tokens.
#These API tokens are needed to run many scripts in LANforge scripts with the functionality these three programs provide.

#Update necessary parts of system
echo Type in your username here
read -r USER

sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install nginx mysql-server nodejs npm -y

#Influx installation
wget https://dl.influxdata.com/influxdb/releases/influxdb2-2.0.7-amd64.deb
sudo dpkg -i influxdb2-2.0.7-amd64.deb
sudo systemctl unmask influxdb
sudo systemctl start influxdb
sudo systemctl enable influxdb

#Grafana installation
sudo apt-get install -y adduser libfontconfig1
wget https://dl.grafana.com/oss/release/grafana_8.0.5_amd64.deb
sudo dpkg -i grafana_8.0.5_amd64.deb
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