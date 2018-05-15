#!/bin/bash
#
# Create the structure of folders for EC2 environment
#

echo "Initializing script for EC2 environment instance"

G_COMPANY="company"

create_directory() {
  DATA_DIR=$1
  if [ ! -d "$DATA_DIR" ]; then
    mkdir -p "$DATA_DIR"
    echo "directory created: $DATA_DIR"
  fi
}

# configuration files
create_directory "/var/$G_COMPANY/conf"

# tools for devops
create_directory "/var/$G_COMPANY/devops"

# specific application directories
create_directory "/var/$G_COMPANY/logs"

# specific web-application directories
create_directory "/var/$G_COMPANY/www"

# specific database-data directory
create_directory "/var/$G_COMPANY/data"

# specific run-pid
create_directory "/var/$G_COMPANY/run"

# specific swagger-documentation directory
create_directory "/var/$G_COMPANY/swagger"


echo "Structure created for instance"