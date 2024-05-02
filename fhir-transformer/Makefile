# Load environment variables
include .env
export $(shell sed 's/=.*//' .env)


REQUIRED_VARS=POSTGRES_HOST \
POSTGRES_PORT \
POSTGRES_DB \
POSTGRES_USER \
POSTGRES_PASSWORD \

# Variables
PYTHON = python3
PIP = pip3
CODE_DIRS = src tests

install-requirements:
	$(PIP) install -r requirements.txt


# Copies .env.example & creates .env script
init-repo:
	cp .env.example .env
	touch $@


check-required-vars:
	missing_vars=""
	for var in $(REQUIRED_VARS); do \
        if ! $$( printenv | grep $$var | grep -qv "PLEASE_SET_ME") && ! $$( cat .env | grep $$var | grep -qv "PLEASE_SET_ME"); then \
            missing_vars+=" $$var"; \
        fi; \
    done; \
    if [ -n "$$missing_vars" ]; then \
        echo "Missing environment variables:$$missing_vars"; \
        exit 1; \
    fi	


format: install-requirements
	isort $(CODE_DIRS)
	black $(CODE_DIRS)

lint: install-requirements
	flake8 $(CODE_DIRS)
	black --check $(CODE_DIRS)


docker-build: check-required-vars
	docker build -t fhir-transformer .

docker-run: check-required-vars
	docker rm -f $(POSTGRES_HOST)
	docker run --name postgres -e POSTGRES_PASSWORD=$(POSTGRES_PASSWORD) -d -p 5432:5432 postgres
	docker build -t fhir-transformer . 
	docker run --rm --link postgres -e POSTGRES_PASSWORD=$(POSTGRES_PASSWORD) fhir-transformer 

build-and-run: check-required-vars
	docker-compose down
	docker-compose build
	docker-compose up -d