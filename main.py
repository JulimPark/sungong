import pandas as pd
import numpy as np
import streamlit as st
import seaborn as sns
from datetime import datetime
import ast
from google.cloud import firestore
from google.oauth2 import service_account
from pytz import timezone
import datetime as dtt
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
    temp_dict = {'시작시간':aaa,'시작스탬프':timestamp1,'마침시간':'-','마침스탬프':'-'}
    
    df11 = pd.DataFrame(temp_dict, index=[0])
    df11['시작시간']= pd.to_datetime(df11['시작시간'])
    
    df11.to_csv('temp_csv.csv',index=False,mode='w')
    st1 = datetime.fromtimestamp(timestamp1)
    st.write(f"시작시간: {aaa}")

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
    df12['시작시간']= pd.to_datetime(df12['시작시간'])
    timestamp11 = df12.iat[0,0]
    timestamp22 = df12.iat[0,1]
    
    bbb = datetime.now(timezone('Asia/Seoul'))
    bbb2 = bbb.timestamp()
    sungong = bbb2 - timestamp22
    st1 = datetime.fromtimestamp(timestamp22)
    et1 = datetime.fromtimestamp(bbb2)
    df12.iat[0,2] = bbb
    df12.iat[0,3] = bbb2
    st.dataframe(df12)
    id_time = f"{stu_id}_{bbb.year}-{format(bbb.month,'02')}-{format(bbb.day,'02')} {format(bbb.hour,'02')}:{format(bbb.minute,'02')}:{format(bbb.second,'02')}"
    doc_ref2 = db2.collection("sungong").document(id_time)
    doc_ref2.set({'학생id':stu_id,'시작시간':timestamp11,
                  '마침시간':bbb,
                 '순공시간':round(sungong,2)})
#     doc_ref2.set({'aa':timestamp11,'bb':bbb})
    st.write(f"마침시간: {bbb}")
    st.header(f"순공시간: {dtt.timedelta(seconds=sungong)}")

start_button = st.button('시작')
end_button = st.button('마침')

if start_button:
  push_start_data2('pinko')
 
if end_button:
  push_end_data('pinko')
