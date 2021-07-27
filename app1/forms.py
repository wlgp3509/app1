from django import forms
from app1.models import Question, Answer

# 21.07.13(최졔)
# QuestionForm 같은 클래스를 장고 폼이라고 부른다
# 장고 폼에는 2가지 폼이 있다.(일반, 모델)

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['subject', 'content']
# ----- 21.07.14(최졔) <질문 등록하기> 제목,내용에 bootstrap 적용
# html에 적용하지 않고 모듈에서 적용하는 이유?
# {{form.as_p}} : 모델 (테이블)의 정보를 받아 form과 요소를 자동으로 생성하는 템플릿 태그 때문에
# 테이블 컬럼 숫자에 관계없이 컬럼을 불러올 수 있다는 장점이 있지만
# html(templete)단에서 스타일을 적용하기 힘든 단점이 있음
# 이러한 단점을 widgets 속성을 이용하여 해당 템플릿(html)로딩시
# 클래스 정보를 전달해주는 방식으로 커버함.
# key값은 해당 컬럼명, value값은 적용할 속성으로 쓴다.
        widgets = {
            # key값 선언
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
        }

        labels = {
            'subject': '제목',
            'content': '내용',
        }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['answer_content']
        labels = {
            'answer_content': '답변내용',
        }