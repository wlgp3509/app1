from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
# views.py의 위치에서 models.py를 찾아 question을 import 하라는 의미
from .models import Question, Answer
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from app1.forms import QuestionForm, AnswerForm
# 21.07.19- 페이징처리 관련 모듈 클래스
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
# 21.07.22 - 자신만 수정가능 관련 모듈
from django.contrib import messages

#  템플릿 태그 종류 AT html
# 1. {% if 요청받은값(question_list) %} : question_list가 있을경우
# 2. {% for 임시변수 in 요청받은값(딕셔너리 키값) %} : 딕셔너리의 키의 value를 반복하여 순차적으로 임시변수에 대입
# 3. {% 임시변수.컬럼 %} : for문에 의해 선언된 임시변수의 컬럼출력

def index(request):
    # request : 외부 사용자의 요청을 받아오는것
    # render : 템플릿을 로딩할 때 사용
    # redirect : URL로 이동시 사용
    # 사용자가 localhost:8000/app1 페이지 접속이라는 요청을 보냈다
    # view -> urls에 어떤 함수를 실행해야 하는지를 확인
    # 21.07.09 질문 목록 가져오기
    # view에서 model단에 요청
    # 요청의 내용 : 조회(Question 테이블/모델 create_date 컬럼을 기준으로 정렬해서 가져옴)
    #          -> 그 결과를 question_list 변수에 저장

    # (GET은 전송방식중 1)
    page = request.GET.get('page', '1')


    question_list = Question.objects.order_by('-create_date')   #내림차순은 앞에 -을 붙여
    # context라는 변수에 딕셔너리 형태로 question_list key와 value를 저장
    # 템플릿단에서 해당 데이터를 쉽게 조회하기 위해

    # 21.07.19 페이징 처리 내용
    # 가져온 데이터를 10개씩 보여주기
    paginater = Paginator(question_list, 10)
    page_obj = paginater.get_page(page)

    context = {'question_list': page_obj}
    # 받은 요청에 대해(request)
    # app1/question.list.html 템플릿을 열어주고
    # 해당 템플릿에 context 변수의 값을 전송
    return render(request, 'app1/question_list.html', context)

#21.07.12(최졔)
def detail(request, question_id):  #요청, id값 파라미터
    # get_object_or_404 : pk에 해당하는 건이 없다면 404페이지 출력
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'app1/question_detail.html', context)



# 21.07.23 답변등록 수정전
# def answer_create(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     question.answer_set.create(answer_content=request.POST.get('answer_content'), create_date=timezone.now())
#
#     return redirect('app1:detail', question_id=question_id)

# 21.07.23 answer_create 수정 (최졔)
# 기존 기능중 로그인하지 않은 사용자도 답변을 달수 있는 문제점으로 인해 수정
# author 컬럼이 추가됨에따라 답변 작성자를 저장하기 위한 코드 수정
@login_required(login_url='common:login')
def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('app1:detail', question_id=question.id)
    else:
        form = AnswerForm()
    context = {'question': question, 'form': form}
    return render(request, 'app1/question_detail.html', context)


# 질문등록 함수 21.07.13(최졔) - 기존내용 백업
# def question_create(request):
#     form = QuestionForm()
#     return render(request, 'app1/question_form.html', {'form': form})

# 21.07.14 (최졔) -- 수정내용 : GET, POST 방식에 대한 처리
# ★★★★ render , redirect 두가지를 참고해!!! ★★★★
# question_form으로 들어올때, 질문을 등록할 때
# 질문을 등록할때 GET vs POST 방식인지 확인
# 이유 : 단순히 질문등록 페이지를 오픈한것인지? (GET - render)
# 질문등록페이지에 데이터를 입력해서 저장한것인지? (POST - redirect)

# 21.07.21 login_required 데코레이터를 추가함으로써
# 만약 질문 등록하기 페이지 이동시 로그인이 안되어있다면 로긘페이지로 먼저 이동시킴
@login_required(login_url='common:login')
def question_create(request):
    if request.method == "POST":       #요청받은 메소드가 포스트인지?
        # forms.py에 설정한 QuestionForm 클래스를 호출
        # request.POST : 사용자가 입력한 데이터를 받아온다
        form = QuestionForm(request.POST)
        # 변수 form에 들어온 값이 올바른값(정상적인 값)인지를 확인
        if form.is_valid():
            # 저장을 하기전 잠시 유보 (co~=F~) << 여기를 통해!
            # question 변수에 from에서 받아온 데이터는 넣어뒀지만 아직 DB로 저장하진 않음
            question = form.save(commit=False)
            # create_date 컬럼을 따로 입력받지 않은 이유?
            # 질문 등록의 날짜 시간의 경우 현재 시간으로 입력받기 위해 view에서 처리
            question.create_date = timezone.now()
            question.author = request.user
            question.save()
            return redirect('app1:index')
    else:
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'app1/question_form.html', context)

#--21.07.21 질문 수정 함수 추가
@login_required(login_url='common:login')
def question_modify(request, question_id):
    # 없는 페이지거나 잘못된 곳으로 갈경우 '없는페이지 error 호출'
    question = get_object_or_404(Question, pk=question_id)

    # 타인이 수정할 수 없게(본인만 수정 가능)
    if request.user != question.author:
        messages.error(request, '수정 권한이 없습니다')
        return redirect('app1:detail', question_id=question.id)

    # 전송방식이 POST인지 (데이터를 받아왔는지) 확인
    # -> question_form으로 접속만 한건지 (이건 GET임)
    if request.method == "POST":
        # <<instance = question>>
        # 인스턴스 파라미터에 question 테이블을 지정해 기존값의 form에 채워넣음
        # 만약 전달받은 데이터가 있다면, 전달받은 입력값을 덮어써서 qustion form을 재생성
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user      # 글쓴이 갖고왕!
            question.modify_date = timezone.now()
            question.save()
            # 수정된 내용 저장을 완료후 question_detail 페이지로 이동
            # 주의사항 : 일반적인 방식으로 redirect 리턴한다면 key(id)값을 찾을수 없음
            #       -> 그러한 상황을 방지하기 위해 question_id에 기존 컬럼의 key값을 반환함 = 120번째줄 question~
            return redirect('app1:detail', question_id=question.id)


    form = QuestionForm(instance=question)
    return render(request, 'app1/question_form.html', {'form': form})

# 21.07.22 질문 삭제 관련 함수
@login_required(login_url='common:login')
def question_delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    if request.user != question.author:
        messages.error(request, '삭제 권한이 없습니다')
        return redirect('app1:detail', question_id=question.id)
    question.delete()
    return redirect('app1:index')

# 21.07.23 답변 수정 함수---------------------------------------------
# 문제: 1. answer_form에서 데이터 입력받으면 해당 내용을 저장하는 부분 구현
#      2. answer_form html 문서를 오픈하는 부분 구현
#      3. 답변 수정은 답변을 작성한 본인만 수정가능하도록
#      4. 반드시 로그인한 사용자만 수정 가능하도록 하세요

@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)

    # 답변수정은 답변 작성자만 수정 가능하게 처리하는 코드 .
    # 답변 작성자와 로그인한 유저가 같은지 확인
    if request.user != answer.author:
        messages.error(request, '수정 권한이 없습니다')
        return redirect('app1:detail', question_id=answer.question.id)

    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user  # 글쓴이 갖고왕!
            answer.modify_date = timezone.now()
            answer.save()
            return redirect('app1:detail', question_id=answer.question.id)
    else:
        form = AnswerForm(instance=answer)
    return render(request, 'app1/answer_form.html', {'form': form})

# 21.07.23 답변삭제
@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)

    if request.user != answer.author:
        messages.error(request, '삭제 권한이 없습니다')
        return redirect('app1:detail', answer_id=answer.id)
    answer.delete()

    form = QuestionForm(instance=answer)
    return redirect('app1:detail', question_id=answer.question.id)


def test(request):
    return render(request, 'app1/template2.html')








# get방식 & post방식        /데이터 전송방식
# get방식 : URL에 파라미터를 붙여서 전송하는 방식
#     -> 속도가 빠르다라는 장점이 있지만 URL에 데이터를 실어서 보내기 때문에
#        보안에 취약하거나, 그외 데이터 전송에 여러가지 제한사항이 있다.
# post방식 : HTML의 BODY 영역에 데이터를 실어 보내는 방식(form)
#           대용량의 데이터를 보낼 수 있고, 주소에 실어 보내지 않기때문에
#           get방식에 비해 보안성 또한 좋다.

# csrf_token : 브라우저에서 작성된 데이터가 올바른 데이터인지, 혹은 진짜 웹 브라우저에서 작성된 데이터인지 판단