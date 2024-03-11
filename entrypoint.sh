#!/bin/bash

# Activate virtual environment (assuming it exists)
source ../bin/activate

# Set Django settings module
export DJANGO_SETTINGS_MODULE="application.settings"

# Apply database migrations
python3 manage.py makemigrations
python3 manage.py migrate

# Start Django development server
python3 manage.py runserver 
```
