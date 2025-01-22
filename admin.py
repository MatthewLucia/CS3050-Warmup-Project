import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import json

cred = credentials.Certificate('cs3050-warmup-project-d7296-firebase-adminsdk-fbsvc-37c75d0990.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

with open('us_states_data.json', 'r') as f:
    data = json.load(f)

for item in data:
    doc_ref = db.collection('us_states_data').document(item['uuid'])
    doc_ref.set(item)
