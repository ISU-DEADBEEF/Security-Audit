#!/bin/bash

# Update and upgrade system packages
apt update && apt upgrade -y

# Create a logger user
adduser --disabled-password --gecos "" logger

# Update sudoers file for logger user
echo "logger ALL=(ALL) NOPASSWD: /usr/local/bin/log_history.sh" | sudo tee -a /etc/sudoers

# Create the logging directory with appropriate permissions
mkdir -p /var/log/Logger
chmod 1777 /var/log/Logger

# Create the logging script
cat << 'EOF' > /usr/local/bin/log_history.sh
#!/bin/bash

# Get the current user
USER=$(whoami)

# Define the log file path
LOG_FILE="/var/log/Logger/${USER}.history"

# Function to append the last command to the log file
log_command() {
    # Get the last executed command from history
    local LAST_COMMAND="$(history 1 | sed 's/^ *[0-9]* *//')"

    # Append the last command to the log file with a timestamp
    echo "$(date '+%Y-%m-%d %H:%M:%S') - ${LAST_COMMAND}" >> "${LOG_FILE}"
}

# Export the function to be used in PROMPT_COMMAND
export -f log_command

# Set PROMPT_COMMAND to log each command before it executes
PROMPT_COMMAND="log_command; $PROMPT_COMMAND"

# Ensure the log file exists and is writable
touch "${LOG_FILE}"
chmod a+rw "${LOG_FILE}"
EOF

# Set permissions for the logging script
chmod 755 /usr/local/bin/log_history.sh

# Configure global shell environment
echo -e "\n# Source the logging script to set up PROMPT_COMMAND for all users\nif [ -f /usr/local/bin/log_history.sh ]; then\n    source /usr/local/bin/log_history.sh\nfi" | sudo tee -a /etc/bash.bashrc

# Add script source line to skeleton user profile
echo "source /usr/local/bin/log_history.sh" | sudo tee -a /etc/skel/.bashrc

# Test logging system with a dummy user
adduser --disabled-password --gecos "" dummy

echo "Installation and setup complete. You can now switch to the 'dummy' user to test logging."
