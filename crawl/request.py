from selenium import webdriver
import requests
import json

res = requests.get('https://1968.freeway.gov.tw/api/getRoadInformation', params={'action': "roadinfo", 'freewayid': '1','from_milepost': 0,'end_milepost': 10000, 'cctv' : True})
# print(res.json())

data = res.json()
cctv = data["response"]["cctv"]

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(cctv, f, ensure_ascii=False, indent=4)