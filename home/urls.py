from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('client/create/', views.create_client, name='create_client')
]