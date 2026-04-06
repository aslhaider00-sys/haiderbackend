from django.urls import path
from . import views

app_name = 'posts' #says designated this url psth inside post app

urlpatterns = [
    path('', views.posts_list, name="list"),
    path('new-post/', views.posts_new, name="new-post"),
    path('<slug:slug>', views.posts_page, name="page"),
]