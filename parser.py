import requests
from bs4 import BeautifulSoup
# import json
import os
# 파이썬이 실행될대 DJAGO_SETTINGS_MODULE이라는 환경변수에
# 현재 프로젝트에 settings.py 파일 경로를 등록
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "websaver.settings")

# 21.07.29 최졔
# parser.py 파일의 위치를 jango에 등록
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 함수의 첫번째줄에 주소랑, 4번째 줄안의 태그들만 수정하면 어디서나 쓸수있엉!!
def parse_blog():
    req = requests.get('https://beomi.github.io/beomi.github.io_old/')
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    titles = soup.select(
        'h3 > a'
    )
    data = {}

    for i in titles:
        data[i.text] = i.get('href')
    return data

    # with open(os.path.join(BASE_DIR, 'result.json'), 'w') as json_file:
    #     json.dump(data, json_file)
