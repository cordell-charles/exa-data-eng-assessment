# Database layer for patient data storage #

# library imports
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Module imports
from config import (
    POSTGRES_DB,
    POSTGRES_HOST,
    POSTGRES_PASSWORD,
    POSTGRES_PORT,
    POSTGRES_USER,
)


def create_tables():
    """
    Create the 'patients' and 'observations' tables in the PostgreSQL db.

    Function first checks if the db exists. If not, a new db is created
    Once created, a 'patients' and 'observations' tables are
    created with the specified schema.
    """

    # Connect to the PostgreSQL server
    connection = psycopg2.connect(
        host=POSTGRES_HOST,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        port=POSTGRES_PORT,
        database=POSTGRES_DB,
    )
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    cursor = connection.cursor()

    # Check if the database exists
    cursor.execute(
        f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{POSTGRES_DB}'"
    )
    exists = cursor.fetchone()

    # If the database doesn't exist, create it
    if not exists:
        cursor.execute(f"CREATE DATABASE {POSTGRES_DB}")
    connection.close()

    # Connect to newly created database
    connection = psycopg2.connect(
        host=POSTGRES_HOST,
        database=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        port=POSTGRES_PORT,
    )

    # Create the 'patients' table
    cursor = connection.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS patients (
            patient_id TEXT PRIMARY KEY,
            name TEXT,
            gender TEXT,
            birth_date DATE
        );
    """
    )

    # Create the 'observations' table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS observations (
            id SERIAL PRIMARY KEY,
            patient_id TEXT REFERENCES patients(patient_id),
            observation_code TEXT,
            observation_value FLOAT,
            observation_unit TEXT,
            observation_date DATE
        );
    """
    )

    connection.commit()
    connection.close()


def insert_data(patient_df, observation_df):
    """
    Function takes in and iterates over the patient_df and observation_df DataFrames
    where it inserts the data into the 'patients' and 'observations' tables, respectively.
    """

    # Connect to the PostgreSQL database
    connection = psycopg2.connect(
        host=POSTGRES_HOST,
        database=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        port=POSTGRES_PORT,
    )
    cursor = connection.cursor()

    # Insert patient data
    for _, row in patient_df.iterrows():
        cursor.execute(
            """
            INSERT INTO patients (patient_id, name, gender, birth_date)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (patient_id) DO NOTHING;
        """,
            (row["patient_id"], row["name"], row["gender"], row["birth_date"]),
        )

    # Insert observation data
    for _, row in observation_df.iterrows():
        cursor.execute(
            """
            INSERT INTO observations (
                patient_id,
                observation_code,
                observation_value,
                observation_unit,
                observation_date
            )
            VALUES (%s, %s, %s, %s, %s)
        """,
            (
                row["patient_id"],
                row["observation_code"],
                row["observation_value"],
                row["observation_unit"],
                row["observation_date"],
            ),
        )

    connection.commit()
    connection.close()
