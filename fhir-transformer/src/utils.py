# Library / Module imports #
import json
import os
from typing import List


def read_fhir_messages(directory: str) -> List[dict]:
    fhir_messages = []
    try:
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            print(f"Patient file: {filepath}")
            with open(filepath, "r") as file:
                fhir_message = json.load(file)
                # print(f"patient file: {filepath} with message: {fhir_messages}")
                fhir_messages.append(fhir_message)
    except Exception as e:
        print(f"error reported: {e}")

    return fhir_messages


# file_path = os.path.join(os.path.dirname(__file__), "../data")
# read_fhir_messages(file_path)
