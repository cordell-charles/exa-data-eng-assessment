import os

import pandas as pd
import pytest
from fhir.resources.observation import Observation
from fhir.resources.patient import Patient

from fhir_scripts.src.fhir_transformers import transform_fhir_messages
from fhir_scripts.src.utils import read_fhir_messages

# Test data
TEST_DATA_DIR = "tests/data"
FHIR_MESSAGES = read_fhir_messages(TEST_DATA_DIR)

# Expected output
EXPECTED_PATIENT_DF = pd.read_csv(
    os.path.join(TEST_DATA_DIR, "expected_patient_df.csv")
)
EXPECTED_OBSERVATION_DF = pd.read_csv(
    os.path.join(TEST_DATA_DIR, "expected_observation_df.csv")
)


@pytest.fixture
def fhir_messages():
    return FHIR_MESSAGES


def test_transform_fhir_messages(fhir_messages):
    patient_df, observation_df = transform_fhir_messages(fhir_messages)

    # Test patient DataFrame
    assert patient_df.equals(EXPECTED_PATIENT_DF)

    # Test observation DataFrame
    assert observation_df.equals(EXPECTED_OBSERVATION_DF)


def test_patient_resource_parsing(fhir_messages):
    for message in fhir_messages:
        if message["resourceType"] == "Bundle":
            for entry in message["entry"]:
                resource = entry["resource"]
                resource_type = resource["resourceType"]

                if resource_type == "Patient":
                    patient = Patient.parse_obj(resource)
                    assert patient.id is not None
                    assert patient.name is not None
                    assert patient.gender is not None
                    assert patient.birthDate is not None


def test_observation_resource_parsing(fhir_messages):
    for message in fhir_messages:
        if message["resourceType"] == "Bundle":
            for entry in message["entry"]:
                resource = entry["resource"]
                resource_type = resource["resourceType"]

                if resource_type == "Observation":
                    observation = Observation.parse_obj(resource)
                    assert observation.subject is not None
                    assert observation.code is not None
                    assert (
                        observation.valueQuantity is not None
                        or observation.valueQuantity is None
                    )
                    assert observation.effectiveDateTime is not None
