from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect

from .models import Blog, Comment, Tag, Like


def home(request):
    blogs = Blog.objects.all()
    paginator = Paginator(blogs, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'home.html', {'page_obj': page_obj})


def detail(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    comments = Comment.objects.filter(blog=blog)  # 해당 blog 객체에 해당하는 Comments 객체들만 가져옴
    tags = blog.tag.all()
    likes = len(Like.objects.filter(blog=blog))  # 해당 blog 객체에 해당하는 Like 객체들만 가져옴
    return render(request, 'detail.html', {'blog': blog, 'comments': comments, 'tags': tags, 'likes': likes})


def new(request):
    tags = Tag.objects.all()
    return render(request, 'new.html', {'tags': tags})


def create(request):
    new_blog = Blog()
    new_blog.title = request.POST.get('title')
    new_blog.content = request.POST.get('content')
    new_blog.image = request.FILES.get('image')
    new_blog.author = request.user

    new_blog.save()
    tags = request.POST.getlist('tags')

    for tag_id in tags:
        tag = Tag.objects.get(id=tag_id)
        new_blog.tag.add(tag)

    return redirect('detail', new_blog.id)


def edit(request, blog_id):
    # edit_blog = get_object_or_404(Blog, pk=blog_id)
    edit_blog = Blog.objects.get(id=blog_id)
    tags = Tag.objects.all()

    if request.user != edit_blog.author:
        return redirect('detail', edit_blog.id)

    return render(request, 'edit.html', {'edit_blog': edit_blog, 'tags':tags})


def update(request, blog_id):
    old_blog = get_object_or_404(Blog, pk=blog_id)
    old_blog.title = request.POST.get('title')
    old_blog.content = request.POST.get('content')
    old_blog.image = request.FILES.get('image')
    old_blog.save()

    old_blog.tag.clear() # 기존 tag 필드 삭제
    tags = request.POST.getlist('tags')
    for tag_id in tags:
        tag = get_object_or_404(Tag, pk=tag_id)
        old_blog.tag.add(tag)

    return redirect('detail', old_blog.id)


def delete(request, blog_id):
    delete_blog = get_object_or_404(Blog, pk=blog_id)
    if request.user == delete_blog.author:
        delete_blog.delete()
        return redirect('home')
    return redirect('detail', delete_blog.id)


# 댓글 입력창 띄우기
def new_comment(request, blog_id):
    # 로그인하지 않았다면 댓글 입력창 못 가고 로그인하기로 이동
    if request.user.is_anonymous:
        return redirect('singin')
    # 로그인했다면
    blog = get_object_or_404(Blog, pk=blog_id)
    return render(request, 'new_comment.html', {'blog': blog})


# 댓글 작성 버튼
def create_comment(request, blog_id):
    comment = Comment()
    comment.content = request.POST.get('content')
    comment.blog = get_object_or_404(Blog, pk=blog_id)
    comment.author = request.user
    comment.save()
    return redirect('detail', blog_id)


def like(request, blog_id):
    if request.user.is_anonymous:
    # 로그인하지 않았다면 좋아요 못 누르고 로그인하기로 이동
        return redirect('login')
    if Like.objects.filter(likedUser=request.user, blog_id=blog_id):
    # "현재 로그인한 사용자"가 "해당 글"에 Like 객체를 만든 것이 존재한다면
        return redirect('detail', blog_id)
    # "현재 로그인한 사용자"가 "해당 글"에 Like 객체를 만든 것이 존재하지 않다면
    like = Like()
    like.blog = get_object_or_404(Blog, pk=blog_id)
    like.likedUser = request.user
    like.save()
    return redirect('detail', blog_id)
