from django import forms
from django.contrib.auth.forms import UserCreationForm   # 회원가입 정보들을 쉽게 저장할수있음
from django.contrib.auth.models import User              # 회원가입 유저들(테이블의 row)

class UserForm(UserCreationForm):
    email = forms.EmailField(label='이메일')

    class Meta:
        model = User
        fields = ("username", "email")

