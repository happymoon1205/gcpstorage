from pymongo import MongoClient
import requests
from google.cloud import storage
import os
from io import BytesIO

# 이미지를 바로 Google Cloud Storage 버킷에 업로드하는 함수
def upload_image_url_to_gcs(bucket_name, url, destination_blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    
    response = requests.get(url)
    
    with BytesIO(response.content) as f:
        blob.upload_from_file(f, content_type='image/jpeg')

#mongoDB와 연결
client = MongoClient('mongodb://[계정아이디]:[비밀번호]@[몽고디비IP]/')
db = client['final']
collection = db['movies']

#연결된 도큐먼트들에서 필요한 정보들 수집 후 로컬에 이미지 저장없이 스토리지에 저장
for i in collection.find().limit(10): # find()로 해야지 for문을 사용가능 10개만 뽑아봄
    url=i['poster_image_url']
    bucket_name = '버킷이름'  # Google Cloud Storage 버킷 이름
    destination_name=f'{str(i["_id"])}.jpg'# 이거를 사진이름으로 해야한다 
    
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] ="키파일 경로"
    upload_image_url_to_gcs(bucket_name, url, destination_name)
