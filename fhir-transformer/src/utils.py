# Library / Module imports
import os
import json
from typing import List

def read_fhir_messages(directory: str) -> List[dict]:
    fhir_messages = []
    try:
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            print(f"Patient file: {filepath}")
            with open(filepath, 'r') as file:
                fhir_message = json.load(file)
                fhir_messages.append(fhir_message)
    except Exception as e:
        print(f"Patient file: {filename}, error reported: {e}")
    
    print(f"fhir messages: {fhir_messages}") 
    return fhir_messages

file_path = r".\data"
read_fhir_messages(file_path)