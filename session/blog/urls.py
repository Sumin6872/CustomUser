from django.urls import path
from . import views


urlpatterns = [
    # READ
    path('', views.home, name='home'), # 127.0.0.1:8000
    path('blog/<int:blog_id>/', views.detail, name='detail'),
    # CREATE
    path('blog/new/', views.new, name='new'),
    path('blog/create/', views.create, name='create'),
    # UPDATE
    path('blog/edit/<int:blog_id>/', views.edit, name='edit'),
    path('blog/update/<int:blog_id>/', views.update, name='update'),
    # DELETE
    path('blog/delete/<int:blog_id>/', views.delete, name='delete'),
    # COMMENT
    path('blog/<int:blog_id>/new_comment/', views.new_comment, name='new_comment'),
    path('blog/<int:blog_id>/create_comment/', views.create_comment, name='create_comment'),
    # LIKE
    path('blog/<int:blog_id>/like', views.like, name="like"),
]