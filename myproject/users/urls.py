from django.urls import path
from . import views

app_name = 'users' #says designated this url psth inside post app

urlpatterns = [
    path('register/', views.register_view, name="register"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('api_login/', views.api_login, name="api_login"),
    path('api_register/', views.api_register, name="api_register"),
    path('profile/', views.get_user_profile, name='user-profile'),  
    path('profile/update/', views.update_user_profile, name='user-profile-update'),  
]