from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from users import views as user_views

from .views import index, results, error404

urlpatterns = [
    path('', index, name="home"),
    path('results/', results, name="results"),
    path('404/', error404, name="404"),
    
    path('login/', auth_views.LoginView.as_view(template_name='webApp/login.html'), name="login"),
    path('register/', user_views.register, name="register"),

]