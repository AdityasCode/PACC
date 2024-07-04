import json

with open('creds.json', 'w') as json_file:
    json.dump({1: 2, 4: 5}, json_file, indent=2)
