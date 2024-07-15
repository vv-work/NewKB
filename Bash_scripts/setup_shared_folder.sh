#!/bin/bash

# Create the shared directory if it doesn't already exist
sudo mkdir -p /home/shared

# Create the group for shared access if it doesn't already exist
sudo groupadd -f sharedgroup

# Add users to the group
sudo usermod -aG sharedgroup julius
sudo usermod -aG sharedgroup 13a4ua

# Change the ownership of the shared directory to root:sharedgroup
sudo chown root:sharedgroup /home/shared

# Set the permissions for the shared directory
sudo chmod 2775 /home/shared

# Ensure the sticky bit is set to maintain group permissions
sudo chmod g+s /home/shared

# Verify the setup
echo "Shared directory setup:"
ls -ld /home/shared
echo "Users in sharedgroup:"
getent group sharedgroup


