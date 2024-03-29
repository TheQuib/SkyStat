#!/bin/bash

# Define paths and names
SOURCE_DIR="/home/skystat"
INSTALL_DIR="/opt/skystat"
FLASK_APP="web.py"
SCRIPT_NAME="main.py"
SERVICE_NAME="skystatweb"
PYTHON_PATH="/usr/bin/python3"  # Change this if you're using a virtualenv

# Copy project files to the install directory
echo "Copying project files to $INSTALL_DIR..."
sudo mkdir -p $INSTALL_DIR
sudo cp -r $SOURCE_DIR/* $INSTALL_DIR

# Create systemd service file for Flask app
echo "Creating systemd service file for the Flask app..."
cat <<EOF | sudo tee /etc/systemd/system/${SERVICE_NAME}.service > /dev/null
[Unit]
Description=Skystat Flask Web Service
After=network.target

[Service]
User=pi
WorkingDirectory=$INSTALL_DIR
ExecStart=$PYTHON_PATH $INSTALL_DIR/$FLASK_APP

Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Enable and start the Flask app service
echo "Enabling and starting the Flask app service..."
sudo systemctl daemon-reload
sudo systemctl enable ${SERVICE_NAME}.service
sudo systemctl start ${SERVICE_NAME}.service

# Create a combined cron job for the script
echo "Creating a cron job for $SCRIPT_NAME to run at startup and every 5 minutes..."
CRON_JOB="@reboot $PYTHON_PATH $INSTALL_DIR/$SCRIPT_NAME >> $INSTALL_DIR/main.log 2>&1\n*/5 * * * * $PYTHON_PATH $INSTALL_DIR/$SCRIPT_NAME >> $INSTALL_DIR/main.log 2>&1"
(crontab -l 2>/dev/null | grep -v -F "$INSTALL_DIR/$SCRIPT_NAME"; echo -e "$CRON_JOB") | crontab -

echo "Installation completed."