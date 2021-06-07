how to run:
create enviroment
python3 -m venv venv1

install requirement:
pip install -r requirement.dev.txt

running:
DEVELOPMENT
- export FLASK_ENV=development
- export FLASK_APP=app
- flask run

running test:
pytest

running background task:
python worker.py