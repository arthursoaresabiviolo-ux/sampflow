from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login-page'),
    path('forgot-password/', views.forgot_password, name='forgot-password-page')
]