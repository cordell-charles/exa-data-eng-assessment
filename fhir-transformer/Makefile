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

docker-build:
	docker build -t fhir-transformer .

docker-run:
	docker run -v /fhir-transformer/data fhir-transformer

docker-run-postgres:
	docker run --name postgres -e POSTGRES_PASSWORD=fhir_password -d -p 5432:5432 postgres
	docker build -t fhir-transformer . 
	docker run --rm --link postgres -e POSTGRES_PASSWORD=fhir_password fhir-transformer 