#!/usr/bin/env bash
# 0-setup_web_static.sh
# Sets up web servers for the deployment of web_static.

# Install Nginx if it is not installed
if ! which nginx > /dev/null; then
    sudo apt-get update
    sudo apt-get install -y nginx
fi

# Create the necessary directories if they don't exist
sudo mkdir -p /data/web_static/releases/test
sudo mkdir -p /data/web_static/shared

# Create a fake HTML file at /data/web_static/releases/test/index.html
echo "<html>
  <head>
  </head>
  <body>
    ALX
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html

# Create the symbolic link /data/web_static/current to /data/web_static/releases/test
# If the symlink already exists, delete and recreate it
if [ -L /data/web_static/current ]; then
    sudo rm /data/web_static/current
fi
sudo ln -s /data/web_static/releases/test /data/web_static/current

# Give ownership of the /data folder to the ubuntu user and group recursively
sudo chown -R ubuntu:ubuntu /data

# Update Nginx configuration to serve the content of /data/web_static/current to hbnb_static
# Create a backup of the default Nginx configuration
sudo cp /etc/nginx/sites-available/default /etc/nginx/sites-available/default.bak

# Update the Nginx config to include the alias for /hbnb_static
sudo sed -i '/server_name _;/a \\n\tlocation /hbnb_static {\n\t\talias /data/web_static/current;\n\t}\n' /etc/nginx/sites-available/default

# Restart Nginx to apply changes
sudo service nginx restart

# Exit the script
exit 0
