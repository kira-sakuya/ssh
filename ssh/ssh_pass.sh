#!/bin/bash

# $1 : user
# $2 : host
# $3 : password
# $4 : command

sed -i '' "/$2/d" $HOME/.ssh/known_hosts
sshpass -p $3 ssh -o StrictHostKeyChecking=no $1@$2 $4