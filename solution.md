# Purpose of file

Purpose of solution.md is to detail any important information to the task and thus solution in order for observers/readers to understand intent and thought process which cannot always be explained through the code.


#  Project structure / Documentation 

The final result for FHIR message transformation containers multple directories all encapsulated under the fhir_scripts directory. Below are sub headings which will go into more details on the purpose of each directory along with the what each code file does.


### fhir_scripts/src
The src directories purpose is to house all the code scripts that executes the FHIR transformation, reading in each patients json file from the data directory, transforming into FHIR messages and adding each patient into a tabular format using postgressql.

- **config.py** - This script is the initial set up which stores credentials for connecting to fhir postgres db 
- **utils.py** - The utils script is part of an extraction process and contains a function `read_fhir_messages` which reads in messages from each patient JSON file and returns a list containers dictionaries of FHIR messages.
- **fhir_transformers.py** - Script is responsibile for transforming FHIR messages into a tabular format. It involves taking the messages as inputs and transforming them into two separate dataframes. Dataframes were used for formatting the data into columns that will be easier to add into postgres table without having to do further formatting. Once created, the db tables are created and data inserted.
- **database.py** - This script is responsible for creating and managing the database tables for storing patient and observation data through two main functions `create_tables` & `insert_data`

### Additional resources

Once the main task was completed, additional work was done to not only aid the developer experience, but to also aid the reviewer in terms of executing the scripts. The purpose of aiding the user is to be able to allow even those with minimal technical experience, the ability to execute and view the database tables easily. Instructions on how to run the project is below but the additional files and resources used for this purpose was:

- **Dockerfile / docker-compose.yaml** - Dockerfile contents are for building a Docker image for the FHIR transformer application, while the docker-compose file runs multiple containers under a single docker network. The purpose of which is to run the FHIR messages scripts, build the postgres container and the adminer container which allows users to view the db contents via a browser.
- **Makefile** - Makefiles are used to aid developer experience by allowing you enclose multiple commands within a single executable command. This helpful so developers do not need to remember multiple commands and can simply document necessary commands used for running programmes. These commands do not just extends to running projects but can also be used to run a series of docker related commands, linting and formatting commands and even terminal / scripting commands.
- **requirements.txt** - Python Dependencies needed for project. 

flake8 files purpose is to add addtional config for 


# How to execute

After cloning the repo to local directory, additional implementations have been added to allow the reviewer minimal effort in order to test and view message DB. The following steps should be completed to successfully test

1. Firstly, ensure you have .env file created within the `fhir_scripts`. This can done by changing directory in fhir_scripts and running the command `Make init-repo` (see Makefile for commands and comments).
2. Supply .env credentials with credentials stored in repo: settings > secrets & variables > actions > variables tab
3. Install all python requirements, run command `make install-requirements` **Please ensure you also have docker installed: https://docs.docker.com/get-docker/** 
4. build docker-compose and execute scripts `make build-and-run`
5. Once containers have been built, feel free to check logs of the fhir container but you can also navigate to `localhost:8080` on your browser where you will be naviagted to admin interface. 
    - To sign in set the system to `PostgreSQL` and fill in credentials with same values in .env file.
    - Once signed in you will see two tables, one for patients, the other for observations with the data supplied.
    - Logs can be checked using `docker logs <container_name>


# Addtional Notes

FHIR Standard: (Fast Healthcare Interoperability Resources) - global industry standard for exchanging healthcare information electronically. The FHIR standard describes data formats and elements (known as "resources") and an application programming interface (API) for exchanging electronic health records (EHR). FHIR resources aim to define the core information contents and structure that is shared by most implementations.

Further analysis showed there is a python package dedicated to the FHIR.

Dependency: fhir.resources = pypi.org/project/fhir.resources/


Pandas - Considering project task involves usage of large datasets of medical data, pandas is also an ideal tool for working with this. 

Dependency: pandas - pypi.org/project/pandas/
