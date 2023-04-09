from django.urls import path

from .views import *


app_name = 'users'

urlpatterns = [
    path('signin/', signin, name='signin'),
    path('signup/', signup, name='signup'),
    path('signout/', signout, name='signout'),
    path('new_profile/', new_profile, name='new_profile'),
    path('create_profile/', create_profile, name='create_profile'),
]
