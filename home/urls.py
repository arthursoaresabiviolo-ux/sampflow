from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('client/create/', views.create_client, name='create_client'),
    path('client/delete/<int:client_id>/', views.delete_client, name='delete_client'),
    path('client/edit/<int:client_id>/', views.edit_client, name='edit_client'),
    path('sample/create/', views.create_sample, name='create_sample'),
    path('sample/edit/<int:sample_id>/', views.edit_sample, name='edit_sample'),
    path('sample/delete/<int:sample_id>/', views.delete_sample, name='delete_sample'),
    path('sample/<int:sample_id>/image/', views.sample_image, name='sample_image'),
]
