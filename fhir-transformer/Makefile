# Variables
PYTHON = python3
PIP = pip3
CODE_DIRS = src tests

install-requirements:
	$(PIP) install -r requirements.txt


format: install-requirements
	isort $(CODE_DIRS)
	black $(CODE_DIRS)

lint: install-requirements
	flake8 $(CODE_DIRS)
	isort --check-only $(CODE_DIRS)
	black --check $(CODE_DIRS)

python-run:
	py ./src/utils.py