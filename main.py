import pandas as pd
import numpy as np
import streamlit as st
import seaborn as sns
from datetime import datetime
import ast
from google.cloud import firestore
from google.oauth2 import service_account
from pytz import timezone
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
    aaa = aaa.astimezone(timezone('Asia/Seoul'))
    timestamp1 = aaa.timestamp()
    temp_dict = {'시작시간':aaa}
    df11 = pd.DataFrame(temp_dict, index=[0])
    df11.to_csv('temp_csv.csv',index=False,mode='w')
    st1 = datetime.fromtimestamp(timestamp1)
    
    st.write(f"시작시간: {st1.year}-{st1.month}-{st1.day} {st1.hour}:{st1.minute}:{st1.second}")
    st.write(f"시작시간: {aaa.year}-{aaa.month}-{aaa.day} {aaa.hour}:{aaa.minute}:{aaa.second}")

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
    bbb = datetime.now(timezone('Asia/Seoul'))
    sungong = bbb - timestamp11
    st1 = datetime.fromtimestamp(timestamp11)
    et1 = datetime.fromtimestamp(bbb)
    
    id_time = f"{stu_id}_{et1.year}-{format(et1.month,'02')}-{format(et1.day,'02')} {format(et1.hour,'02')}:{format(et1.minute,'02')}:{format(et1.second,'02')}"
    doc_ref2 = db2.collection("sungong").document(id_time)
    doc_ref2.set({'학생id':stu_id,'시작시간':f"{st1.year}-{format(st1.month,'02')}-{format(st1.day,'02')} {format(st1.hour,'02')}:{format(st1.minute,'02')}:{format(st1.second,'02')}",
                  '마침시간':f"{et1.year}-{format(et1.month,'02')}-{format(et1.day,'02')} {format(et1.hour,'02')}:{format(et1.minute,'02')}:{format(et1.second,'02')}",
                 '순공시간':sungong})
    st.write(f"마침시간: {et1.year}-{et1.month}-{et1.day} {et1.hour}:{et1.minute}:{et1.second}")
    st.header(f"순공시간: {round(sungong,2)}초")

start_button = st.button('시작')
end_button = st.button('마침')

if start_button:
  push_start_data2('pinko')
 
if end_button:
  push_end_data('pinko')
