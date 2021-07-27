from django.db import models
from django.contrib.auth.models import User         #auth컬럼에 user id를 갖고오기 위함 (20번째줄)

# Create your models here.
# 질문과 답변 테이블 생성(21.7.8 최지혜 작성)
# 질문 테이블 : Question
# 질문 제목 : subject
# 질문내용 : content
# 질문 작성일자 :create_date
# 답변 테이블 : Answer

#----------------질문 테이블
class Question(models.Model):
    subject = models.CharField(max_length=100)
    content = models.TextField()
    create_date = models.DateTimeField()

    # -- 21.07.21--컬럼 추가(글쓴이 author)---------------
    # author : 사용자 ID
    # on_delete = models.CASCADE : User에 있는 값이 삭제되면 해당 값과 연결된 Question 테이블의 데이터를 삭제 하라는 의미
    # 개인필기 ! 회원탈퇴하면 알수없음<회원이 작성한 글들은 모조리 삭제됨
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # 21.07.21- 수정관련 컬럼
    # modify_date 컬럼 : 작성한 질문에 대한 수정일자
    # null=True : 해당 컬럼에 Null값을 허용
    # blank=True : 폼 데이터 검사시 값이 없어도 됨
    modify_date = models.DateTimeField(null=True, blank=True)


    def __str__(self):      # subject값을 id값이 아닌 문자열 값 그대로 보여주기위함
        return self.subject



#----------------답변 테이블
# 답변 내용 : Answer_content
# 답변 작성일자 : create_date
# 질문 제목 : question(어떤 질문에대한 답변인지를 알아야 하기 때문)
class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_content = models.TextField()
    create_date = models.DateTimeField()
    # null=True 컬럼에 null값 허용
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    modify_date = models.DateTimeField(null=True, blank=True)