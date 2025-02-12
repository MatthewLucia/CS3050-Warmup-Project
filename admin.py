import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import json

# Login to Firebase
cred = credentials.Certificate('cs3050-warmup-7457f-firebase-adminsdk-fbsvc-998bc9893a.json')
firebase_admin.initialize_app(cred)

# Connect to Firestore DB
db = firestore.client()

# Load the data from JSON file
with open('us_states_data.json', 'r') as f:
    data = json.load(f)

for item in data:
    doc_ref = db.collection('us_states_data').document(item['uuid'])
    doc_ref.set(item)
