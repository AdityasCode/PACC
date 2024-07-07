import json
import os

keys = [
    "type",
    "project_id",
    "private_key_id",
    "private_key",
    "client_email",
    "client_id",
    "auth_uri",
    "token_uri",
    "auth_provider_x509_cert_url",
    "client_x509_cert_url",
    "universe_domain"
]

# Create a dictionary from environment variables
creds = {key: os.getenv(key.lower()) for key in keys}

# Write the dictionary to a JSON file

json_file = open(r"creds.json", "w")
json.dump(creds, json_file, indent=2)
json_file.close()
