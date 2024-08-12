# Security-Audit

Security-Audit is a server/host security logging system designed to enhance your network's security posture. It captures critical system events, including user history, login attempts, and port usage, and logs this information to a central system for easy analysis and monitoring.

## Features

- **System Logging for SSH:** Capture and log all SSH activities, ensuring all access attempts are tracked.
- **Port Usage Monitoring:** Record and monitor port usage to detect any unauthorized access or suspicious activity.
- **Login History Tracking:** Maintain a detailed log of all login attempts, successful or otherwise, to your server.
- **Command History Logging:** Track all commands executed on the system, helping to identify potentially harmful actions.
- **Central Logging System:** Consolidate logs from multiple sources into a single, easy-to-manage location.
- **User-Friendly Output:** Generate clear and concise log reports for quick analysis.

## Installation Automatic
Swtich to root `su -`

download file `setup_security_audit.sh`
OR 
Make a file nammed `setup_security_audit.sh`
```
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
PROMPT_COMMAND="$PROMPT_COMMAND; log_command;"

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
```

Update permissions to execute
`chmod +x setup_security_audit.sh`

Run the file as root
`sudo ./setup_security_audit.sh`

## Installation Manuel

Follow these steps to install and set up Security-Audit:

### Upgrades and Dependencies

First, update and upgrade the system packages:

```bash
sudo su
apt update && apt upgrade -y
```

### Create Logger User

Create a user for logging purposes:

```bash
adduser logger
visudo
```

Add the following line to the bottom of the sudoers file:

```plaintext
logger ALL=(ALL) NOPASSWD: /usr/local/bin/log_history.sh
```

### Install Logging Script

Create and edit the logging script file at `/usr/local/bin/log_history.sh`:

```bash
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
mkdir -p "/var/log/Logger"
touch "${LOG_FILE}"
chmod a+rw "${LOG_FILE}"
```

Change the permissions of the script:

```bash
chmod 755 /usr/local/bin/log_history.sh
```

### Configure Global Shell Environment

Edit the global bash configuration file `/etc/bash.bashrc` to source the logging script for all users:

```bash
# Source the logging script to set up PROMPT_COMMAND for all users
if [ -f /usr/local/bin/log_history.sh ]; then
    source /usr/local/bin/log_history.sh
fi
```

Add the script source line to the skeleton user profile:

```bash
echo "source /usr/local/bin/log_history.sh" | sudo tee -a /etc/skel/.bashrc
```

Set the permissions for the logging directory:

```bash
chmod 1777 /var/log/Logger
```

## Testing

Create a dummy user and test the logging system:

```bash
adduser dummy
```

Switch to the dummy user and run some commands:

```bash
su dummy
ls
pwd
exit
```

Check the log file for the dummy user:

```bash
ls /var/log/Logger/
tail /var/log/Logger/dummy.history
```

## Usage

Security-Audit is designed to run seamlessly with bash commands. Users must have access to bash to operate and interact with the system's logging features.

## Requirements

- Bash shell
- Access to a central logging server
- Appropriate permissions for logging configuration

## Contributing

Security-Audit is an open-source project. We welcome contributions from the community. Feel free to fork the project, make modifications, and submit pull requests.

## License

Security-Audit is released under an open-source license, allowing free use, modification, and distribution of the software.

---

For more information, questions, or support, please contact the project maintainers.
