#!/bin/bash
sudo dnf install virtualenv -y
su -l lanforge -c "cd ~ && python3 -m venv lanforge_env"
su -l lanforge -c "echo 'source ~/lanforge_env/bin/activate' >> ~/.bashrc"
echo "Please restart your terminal, your virtualenv will activate automtically"
