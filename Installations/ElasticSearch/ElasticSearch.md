# Elasticsearch Installation Guide

## Requirements

### Verify Java Installation
- Check if Java is installed on your system:
```bash
java -version
```

### Update System
```bash
sudo apt update
```

## Download Elasticsearch
- Navigate to the installation directory and download Elasticsearch:

```bash
cd /usr/local
sudo mkdir elasticsearch
sudo wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.11.0-amd64.deb
sudo wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.11.0-amd64.deb.sha512
sudo shasum -a 512 -c elasticsearch-8.11.0-amd64.deb.sha512
sudo dpkg -i elasticsearch-8.11.0-amd64.deb
```

### Running Elasticsearch with systemd
- Reload systemd, enable, start, stop Elasticsearch, and view logs:

```bash
sudo /bin/systemctl daemon-reload
sudo /bin/systemctl enable elasticsearch.service
sudo systemctl start elasticsearch.service
sudo systemctl stop elasticsearch.service
sudo journalctl --unit elasticsearch
```


