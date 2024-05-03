# Main FHIR Transformer script #

# Library imports
import pandas as pd
from fhir.resources.observation import Observation
from fhir.resources.patient import Patient

from database import create_tables, insert_data

# custom module imports
from utils import read_fhir_messages


def transform_fhir_messages(fhir_messages):
    """
    Transform FHIR messages into tabular format (DataFrames).
    """
    patient_data = []
    observation_data = []

    for message in fhir_messages:
        if message["resourceType"] == "Bundle":
            for entry in message["entry"]:
                resource = entry["resource"]
                resource_type = resource["resourceType"]

                if resource_type == "Patient":
                    # Parse Patient resource and extract relevant data
                    patient = Patient.parse_obj(resource)
                    name_components = patient.name[0]
                    full_name = " ".join(
                        [
                            (
                                " ".join(name_components.prefix)
                                if name_components.prefix
                                else ""
                            ),
                            " ".join(name_components.given),
                            name_components.family,
                        ]
                    )
                    patient_data.append(
                        {
                            "patient_id": patient.id,
                            "name": full_name,
                            "gender": patient.gender,
                            "birth_date": patient.birthDate.isoformat(),
                        }
                    )

                elif resource_type == "Observation":
                    # Parse Observation resource and extract relevant data
                    observation = Observation.parse_obj(resource)
                    observation_data.append(
                        {
                            "patient_id": observation.subject.reference.split(":")[-1],
                            "observation_code": observation.code.coding[0].code,
                            "observation_value": (
                                observation.valueQuantity.value
                                if observation.valueQuantity
                                else None
                            ),
                            "observation_unit": (
                                observation.valueQuantity.unit
                                if observation.valueQuantity
                                else None
                            ),
                            "observation_date": observation.effectiveDateTime.isoformat(),
                        }
                    )

    # Create DataFrames and supply with extracted data lists
    patient_df = pd.DataFrame(patient_data)
    observation_df = pd.DataFrame(observation_data)

    return patient_df, observation_df


if __name__ == "__main__":
    # Read FHIR messages from the data directory
    fhir_messages = read_fhir_messages("data/")

    # Transform FHIR messages into DataFrames
    patient_df, observation_df = transform_fhir_messages(fhir_messages)
    print(patient_df)
    print(observation_df)

    # Create tables and insert data from the DataFrames into postgres tables
    create_tables()
    insert_data(patient_df, observation_df)
