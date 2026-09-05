from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('client/create/', views.create_client, name='create_client'),
    path('client/delete/<int:client_id>/', views.delete_client, name='delete_client'),
    path('client/edit/<int:client_id>/', views.edit_client, name='edit_client')
]