"""Defines URL patterns for users."""
from django.urls import path, re_path, include
from django.contrib.auth import views as auth_views

from . import views

app_name = "users"
urlpatterns = [
    #login page
    re_path(r'^login/$', auth_views.LoginView.as_view(
    template_name='users/login.html'), name='login'),
    #logout
    re_path(r'^logout/$', views.logout_view, name='logout'),
    #register
    re_path(r'^register/$', views.register, name='register'),

]
