from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
# views.py의 위치에서 models.py를 찾아 question을 import 하라는 의미
from .models import Question
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from app1.forms import QuestionForm

#  템플릿 태그 종류 AT html
# 1. {% if 요청받은값(question_list) %} : question_list가 있을경우
# 2. {% for 임시변수 in 요청받은값(딕셔너리 키값) %} : 딕셔너리의 키의 value를 반복하여 순차적으로 임시변수에 대입
# 3. {% 임시변수.컬럼 %} : for문에 의해 선언된 임시변수의 컬럼출력

def index(request):
    #21.07.09 질문 목록 가져오기
    question_list = Question.objects.order_by('-create_date')   #내림차순은 앞에 -을 붙여
    context = {'question_list': question_list}
    return render(request, 'app1/question_list.html', context)

#21.07.12(최졔)
def detail(request, question_id):  #요청, id값 파라미터
    # get_object_or_404 : pk에 해당하는 건이 없다면 404페이지 출력
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    print(question)
    return render(request, 'app1/question_detail.html', context)

def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    question.answer_set.create(answer_content=request.POST.get('answer_content'), create_date=timezone.now())
    # redirect : 함수에 전달된 값을 참고하여 페이지 이동을 수행하는 함수
    return redirect('app1:detail', question_id=question_id)

# 질문등록 함수 21.07.13(최졔) - 기존내용 백업
# def question_create(request):
#     form = QuestionForm()
#     return render(request, 'app1/question_form.html', {'form': form})

# 21.07.14 (최졔) -- 수정내용 : GET, POST 방식에 대한 처리
# question_form으로 들어올때, 질문을 등록할 때
def question_create(request):
    if request.method == "POST":       #요청받은 메소드가 포스트인지?
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.create_date = timezone.now()
            question.save()
            return redirect('app1:index')
    else:
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'app1/question_form.html', context)




# get방식 & post방식        /데이터 전송방식
# get방식 : URL에 파라미터를 붙여서 전송하는 방식
#     -> 속도가 빠르다라는 장점이 있지만 URL에 데이터를 실어서 보내기 때문에
#        보안에 취약하거나, 그외 데이터 전소엥 여러가지 제한사항이 있다.
# post방식 : HTML의 BODY 영역에 데이터를 실어 보내는 방식(form)
#           대용량의 데이터를 보낼 수 있고, 주소에 실어 보내지 않기때문에
#           get방식에 비해 보안성 또한 좋다.

# csrf_token : 브라우저에서 작성된 데이터가 올바른 데이터인지, 혹은 진짜 웹 브라우저에서 작성된 데이터인지 판단