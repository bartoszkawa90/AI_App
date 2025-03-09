#!/bin/zsh

# Check if an argument is passed
if [ -z "$1" ]; then
    echo "Usage: $0 <flask_app_name>"
    exit 1
fi

# Set Flask environment variables
# $1 is a name of main file without extension, for example in this case simply main
export FLASK_APP=$1
export FLASK_ENV=development

# Run Flask application
flask run

