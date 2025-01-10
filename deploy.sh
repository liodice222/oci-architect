#!/bin/bash

# Update the system
sudo dnf update -y

# Install required packages
sudo dnf install nginx git python3 python3-pip -y

# Start and enable Nginx
sudo systemctl enable --now nginx.service

# Configure firewall to allow HTTP and HTTPS traffic
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload

# Set SELinux to allow httpd to connect to the network
sudo setsebool -P httpd_can_network_connect 1

# Set SELinux to permissive mode
sudo sed -i 's/^SELINUX=.*/SELINUX=permissive/' /etc/selinux/config
sudo setenforce 0

# Remove the default Nginx configuration
sudo rm /etc/nginx/conf.d/default.conf

# Clone GitHub Repo

APP_DIR="/git/myapp"

sudo mkdir -p "$(dirname "APP_DIR")"
sudo chown $USER:$USER "$(dirname "$APP_DIR")"

REPO_URL="https://github.com/liodice222/oci-architect"

if [ -d "$APP_DIR" ]; then
    echo "Directory $APP_DIR already exists. Removing it."
    sudo rm -rf "$APP_DIR"
fi

git clone "$REPO_URL" "$APP_DIR"

# Navigate to the application directory
cd "$APP_DIR" || exit

# Install Python dependencies
sudo pip3 install -r requirements.txt

# Set up Gunicorn service
sudo tee /etc/systemd/system/your-app.service > /dev/null <<EOL
[Unit]
Description=Gunicorn instance to serve your Flask app
After=network.target

[Service]
User=nginx
Group=nginx
WorkingDirectory=$APP_DIR
ExecStart=/usr/local/bin/gunicorn --workers 3 --bind unix:$APP_DIR/your-app.sock wsgi:app

[Install]
WantedBy=multi-user.target
EOL

# Start and enable the Gunicorn service
sudo systemctl start myapp
sudo systemctl enable myapp

# Create an Nginx configuration for the app
sudo tee /etc/nginx/conf.d/your-app.conf > /dev/null <<EOL
server {
    listen 80;
    server_name _;

    location / {
        include proxy_params;
        proxy_pass http://unix:$APP_DIR/your-app.sock;
    }
}
EOL

# Restart Nginx to apply the configuration
sudo systemctl restart nginx

# Print the public IP for access
PUBLIC_IP=$(curl -s ifconfig.me)
echo "Deployment completed successfully! Access your app at http://$PUBLIC_IP"
