# from django.contrib.auth import authenticate
# from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect, get_object_or_404


from .forms import CustomUserSignupForm, CustomUserSigninForm
from .models import CustomUser, Profile


def signup(request):
    form = CustomUserSignupForm()
    if request.method == "POST":
        form = CustomUserSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    return render(request, "newSignup.html", {"form": form})


def signin(request):
    form = CustomUserSigninForm()
    if request.method == 'POST':
        form = CustomUserSigninForm(request, request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("home")
    return render(request, "newSignin.html", {"form": form})


def signout(request):
    logout(request)
    return redirect("home")


def new_profile(request):
    # 로그인하지 않았다면 프로필 누르더라도 계속 홈으로 이동
    if request.user.is_anonymous:
        return redirect('home')
    # 로그인했다면 해당 user의 profile 보기
    profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, 'newProfile.html', {"profile":profile})


def create_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        profile.nickname = request.POST.get('nickname')
        profile.image = request.FILES.get('image')
        profile.save()
        return redirect('users:new_profile')

    return render(request, 'newProfile.html', {'profile': profile})

#
# # 회원가입
# def signup(request):
#     if request.method == 'POST':
#         if request.POST['password1'] == request.POST['password2']:
#             user = User.objects.create_user(
#                 username=request.POST['username'],
#                 password=request.POST['password1'],
#                 email=request.POST['email'],)
#             profile = Profile(user=user, nickname=request.POST['nickname'], image=request.FILES.get('profile_image'))
#             profile.save()
#
#             auth.login(request, user)
#             return redirect('/')
#         return render(request, 'signup.html')
#     return render(request, 'signup.html')
#
# # 로그인
# def login(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             auth.login(request, user)
#             return redirect('/')
#         else:
#             return render(request, 'login.html')
#     else:
#         return render(request, 'login.html')
#
# # 로그아웃a
# def logout(request):
#   auth.logout(request)
#   return redirect('home')
