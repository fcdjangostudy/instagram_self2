from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.urls import reverse

from .decorators import post_owner
from .forms import PostForm
from .forms import CommentForm
from .models import Post, Comment

User = get_user_model()


def post_list(request):
    posts = Post.objects.all()
    context = {
        'posts': posts,
    }
    return render(request, 'post/post_list.html', context)


def post_detail(request, post_pk):
    try:
        post = Post.objects.get(pk=post_pk)
    except Post.DoesNotExist as e:
        url = reverse('post:post_list')
        return HttpResponseRedirect(url)
    template = loader.get_template('post/post_detail.html')
    context = {
        'post': post,
    }
    rendered_string = template.render(context=context, request=request)
    return HttpResponse(rendered_string)


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            # ModelForm의 save()메서드를 사용해서 Post객체를 가져옴
            post = form.save(author=request.user)
            return redirect('post:post_detail', post_pk=post.pk)
    else:
        # post/post_create.html을 render해서 리턴
        form = PostForm()
    context = {
        'form': form,
    }
    return render(request, 'post/post_create.html', context)


@post_owner
@login_required
def post_modify(request, post_pk):
    # 현재 수정하고자하는 Post객체
    post = Post.objects.get(pk=post_pk)

    if request.method == 'POST':
        form = PostForm(data=request.POST, files=request.FILES, instance=post)
        form.save()
        return redirect('post:post_detail', post_pk=post.pk)
    else:
        form = PostForm(instance=post)
    context = {
        'form': form,
    }
    return render(request, 'post/post_modify.html', context)


@post_owner
@login_required
def post_delete(request, post_pk):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=post_pk)
        post.delete()
        return redirect('post:post_list')
    else:
        # post_delete시에 확인창 띄워주기
        pass


@login_required
def comment_create(request, post_pk):
    form = CommentForm(data=request.POST)
    form.save(post=Post.objects.get(pk=post_pk), author=request.user)
    return redirect('post:detail', post_pk=post_pk)


def comment_modify(request, post_pk, co_pk):
    comment = Comment.objects.get(pk=co_pk)
    if request.method == 'GET':
        form = CommentForm(instance=comment)
        context = {
            'form': form
        }
        return render(request, 'post/comment_modify.html', context)
    else:
        form = CommentForm(data=request.POST, instance=comment)
        form.save()
        return redirect('post:detail', post_pk=post_pk)


def comment_delete(request, pk, co_pk):
    comment = Comment.objects.get(pk=co_pk)
    comment.delete()
    return redirect('post:detail', post_pk=pk)


def post_anyway(request):
    return redirect('post:post_list')
