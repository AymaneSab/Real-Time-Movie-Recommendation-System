# Kibana Installation Guide

## Requirements

### Verify Java Installation
- Check if Java is installed on your system:
```bash
java -version
```

### Update System
- Update the system before proceeding:

```bash
sudo apt update
```

## Download Kibana
- Navigate to the installation directory and download Kibana:

```bash
cd /usr/local
sudo mkdir kibana
sudo wget https://artifacts.elastic.co/downloads/kibana/kibana-7.17.14-amd64.deb
sudo shasum -a 512 kibana-7.17.14-amd64.deb
sudo dpkg -i kibana-7.17.14-amd64.deb
Running Kibana with systemd
Reload systemd, enable, start, stop Kibana:
```
## Running Kiubana with systemmd

```bash
sudo /bin/systemctl daemon-reload
sudo /bin/systemctl enable kibana.service
sudo systemctl start kibana.service
sudo systemctl stop kibana.service
```
