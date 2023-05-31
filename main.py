import pandas as pd
import numpy as np
import streamlit as st
import seaborn as sns
from datetime import datetime
import ast
from google.cloud import firestore
from google.oauth2 import service_account

# Authenticate to Firestore with the JSON account key.
import json
key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds, project="test-project-6e03a")
doc_ref = db.collection("sungong").document("test_timer")

# Then get the data at that reference.
doc = doc_ref.get()

# Let's see what we got!
st.write("The id is: ", doc.id)
st.write("The contents are: ", doc.to_dict())