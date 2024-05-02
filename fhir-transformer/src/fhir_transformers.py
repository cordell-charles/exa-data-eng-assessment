### Main FHIR Transformer script ###

# Library imports
import pandas as pd
from fhir.resources.observation import Observation
from fhir.resources.patient import Patient

# custom module imports
from utils import read_fhir_messages


def transform_fhir_messages(fhir_messages):
    patient_data = []
    observation_data = []

    for message in fhir_messages:
        if message["resourceType"] == "Bundle":
            for entry in message["entry"]:
                resource = entry["resource"]
                resource_type = resource["resourceType"]

                if resource_type == "Patient":
                    patient = Patient.parse_obj(resource)
                    patient_data.append(
                        {
                            "patient_id": patient.id,
                            "name": patient.name[0].text,
                            "gender": patient.gender,
                            "birth_date": patient.birthDate.isoformat(),
                        }
                    )

                elif resource_type == "Observation":
                    observation = Observation.parse_obj(resource)
                    observation_data.append(
                        {
                            "patient_id": observation.subject.reference,
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

    patient_df = pd.DataFrame(patient_data)
    observation_df = pd.DataFrame(observation_data)

    return patient_df, observation_df


if __name__ == "__main__":
    fhir_messages = read_fhir_messages("data/")
    patient_df, observation_df = transform_fhir_messages(fhir_messages)
    print(patient_df)
    print(observation_df)
