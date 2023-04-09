from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import CustomUser


# 회원가입 폼
class CustomUserSignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ['username']


# 로그인(인증) 폼
class CustomUserSigninForm(AuthenticationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ['username']
