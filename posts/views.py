from django.shortcuts import render
from .models import Post
# from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from . import forms
# Create your views here.
@login_required(login_url="/users/login/")
def posts_list(request):
    posts = Post.objects.all()  .order_by('-date')                #dic post and its data parang key value
    return render(request, 'posts/posts_list.html', {'posts': posts})

def posts_page(request, slug):
    # return HttpResponse(slug)
    post = Post.objects.get(slug=slug)             #dic post and its data parang key value
    return render(request, 'posts/post_page.html', {'post': post })

#check if this function runs if the user is login if not redirect to login url
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
    return render(request, 'posts/posts_new.html', {'form': form })
