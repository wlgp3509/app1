from django.apps import AppConfig

# 셋팅34번째 줄에 >> 'app1.apps.App1Config',<<이걸 추가시켜야 app1을 장고가 인식할 수 있음
# (DB관련 작업에 대한 내용)
# 장고는 models.py를 이용해서 DB테이블을 생성한다.
# 모델은 앱에 종속되어있다
class App1Config(AppConfig):
    name = 'app1'
