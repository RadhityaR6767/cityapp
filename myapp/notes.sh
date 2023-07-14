#!/bin/bash

# Using venv python to get requirements.txt
python3 -m venv project_env
source project_env/bin/activate
# VVV
pip install flask
pip install elasticsearch==7.17.9
pip install python-dotenv
pip install requests
pip freeze > requirements.txt
# VVV
deactivate
rm -rf project_env
