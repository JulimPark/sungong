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
def call_data(docu_name):
    key_dict = json.loads(st.secrets["textkey"])
    creds = service_account.Credentials.from_service_account_info(key_dict)
    db = firestore.Client(credentials=creds, project="test-project-6e03a")
    doc_ref = db.collection("sungong").document(docu_name)

    # Then get the data at that reference.
    doc = doc_ref.get()
    doc_dic = doc.to_dict()
    return doc_dic

def push_start_data2(stu_id):
    aaa = datetime.now()
    timestamp1 = datetime.now()
    temp_dict = {'시작시간':timestamp1}
    df11 = pd.DataFrame(temp_dict, index=[0])
    df11.to_csv('temp_csv.csv',index=False,mode='w')

def push_start_data(stu_id):
    global id_time
    key_dict = json.loads(st.secrets["textkey"])
    creds = service_account.Credentials.from_service_account_info(key_dict)
    db2 = firestore.Client(credentials=creds, project="test-project-6e03a")
    # Create a reference to the Google post.
    start_time = datetime.now()
    id_time = f"{stu_id}_{str(start_time)}"
    doc_ref2 = db2.collection("sungong").document(id_time)
    doc_ref2.set({'학생id':stu_id,'시작시간':start_time,'마침시간':0})
    

def push_end_data(stu_id):
    key_dict = json.loads(st.secrets["textkey"])
    creds = service_account.Credentials.from_service_account_info(key_dict)
    db2 = firestore.Client(credentials=creds, project="test-project-6e03a")
    df12 = pd.DataFrame(pd.read_csv('temp_csv.csv'))
    timestamp11 = df12.iat[0,0]
    end_time = datetime.now()
    sungong = end_time - timestamp11
    id_time = f"{stu_id}_{str(sungong)}"
    doc_ref2 = db2.collection("sungong").document(id_time)
    doc_ref2.set({'학생id':stu_id,'시작시간':timestamp11,'마침시간':end_time})

start_button = st.button('시작')
end_button = st.button('마침')

if start_button:
  push_start_data2('pinko')
 
if end_button:
  push_end_data('pinko')
