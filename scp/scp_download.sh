#!/bin/bash

# $1 = host
# $2 = local file
# $3 = remote file
# $4 = user

sed -i '' "/$1/d" "$HOME/.ssh/known_hosts" 2>/dev/null
scp -o StrictHostKeyChecking=no "$4"@"$1":"$3" "$2"