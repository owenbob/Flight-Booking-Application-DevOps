#!/bin/bash


set - e

set -o pipefail # if any code doesn't return 0, exit the script

DIR="migrations" 

# function to ensure proper set up of migrations
function set_migrations(){
    if [ -d "$DIR" ]
    then 
        # if migrations folder exists
        echo "Directory migrations already exists"
        python manage.py db migrate && python manage.py db upgrade
    else
        # otherwise
        echo "Directory migrations does not exist"
        python manage.py db init &&python manage.py db migrate && python manage.py db upgrade
    fi
}

# function to start server
function start_server(){
    python run.py
}

set_migrations && start_server
exit 0