from django.db import models

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