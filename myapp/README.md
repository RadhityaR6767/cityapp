# Using venv python to get requirements.txt
python3 -m venv project_env
source project_env/bin/activate
VVV
pip install flask
pip install elasticsearch
pip freeze > requirements.txt
VVV
deactivate
rm -rf project_env