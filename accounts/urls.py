from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_login, name='login'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('logout/', views.user_logout, name='logout')
]