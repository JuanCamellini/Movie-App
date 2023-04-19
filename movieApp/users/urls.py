from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from .views import (
    profile,
    favoritemovies,
    favoriteseries,
    userrate,
    userfavoritegrid,
    register
    )

urlpatterns = [
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('profile/', profile, name="profile"),
    
    path('favoritemovies/', favoritemovies, name="favoritemovies"),
    path('ratedmovies/', userrate, name="userrate"),
    path('favoritegrid/', userfavoritegrid, name="userfavoritegrid"),

    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='webApp/password-reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='webApp/password-reset-done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('change-password/', auth_views.PasswordChangeView.as_view(template_name='users/change-password.html'), name='password_change'),
    path('change-password/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='users/change-password-done.html'),name='password_change_done'),


    ]