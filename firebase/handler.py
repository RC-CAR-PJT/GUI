import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import pytz
import random as rd
from typing import Dict

# Firebase 초기화 (앱이 이미 초기화되어 있으면 재초기화하지 않음)
if not firebase_admin._apps:
    cred = credentials.Certificate('fb_rc_key.json')
    firebase_admin.initialize_app(cred)

# Firestore 클라이언트
db = firestore.client()
korea_timezone = pytz.timezone("Asia/Seoul")


def write_data(collection_name: str, data: Dict):
    current_time = datetime.now(korea_timezone)
    time_doc = current_time.strftime("%Y-%m-%d %H:%M:%S")
    doc_ref = db.collection(collection_name).document(time_doc)
    doc_ref.set(data)


def read_data(collection_name: str) -> Dict:
    collection_ref = db.collection(collection_name)
    docs = collection_ref.stream()
    return {doc.id: doc.to_dict() for doc in docs}
