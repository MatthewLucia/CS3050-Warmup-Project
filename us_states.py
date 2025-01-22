import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import json

# Login to Google Firestore
cred = credentials.Certificate('path/to/private-key.json')
firebase_admin.initialize_app(cred)

# Connect to db
db = firestore.client()

# Read in data from JSON to db
with open('us_states_data.json', 'r') as f:
    data = json.load(f)

for item in data:
    doc_ref = db.collection('us_states_data').document(item['uuid'])
    doc_ref.set(item)
