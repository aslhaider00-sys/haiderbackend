from django.shortcuts import render
from .models import Post
from django.contrib.auth.decorators import login_required
from . import forms
from .serializer import PostSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.

def posts_list(request):
    posts = Post.objects.all().order_by('-date')
    return render(request, 'posts/posts_list.html', {'posts': posts})

def posts_page(request, slug):
    post = Post.objects.get(slug=slug)
    return render(request, 'posts/post_page.html', {'post': post})

@login_required(login_url="/users/login/")
def posts_new(request):
    if request.method == 'POST':
        form = forms.CreatePost(request.POST, request.FILES)
        if form.is_valid():
            newpost = form.save(commit=False)
            newpost.author = request.user
            newpost.save()
    else:
        form = forms.CreatePost()
    return render(request, 'posts/posts_new.html', {'form': form})

@api_view(['GET'])
def demonstration_api(request):
    posts = Post.objects.all().order_by('title')
    serializer = PostSerializer(posts, many=True, context={'request': request})
    return Response(serializer.data)