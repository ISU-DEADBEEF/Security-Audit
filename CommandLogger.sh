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
