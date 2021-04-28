#! /usr/bin/env sh

set -e 

# Start the nginx service
nginx
service nginx start

# Make sure the dagit interface is up on port 3000
dagit -h '127.0.0.1' -p "3000" -w ./workspace.yaml