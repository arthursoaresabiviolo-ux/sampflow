from django.shortcuts import render, redirect
from .models import Client

def home(request):
    if request.method == 'GET':
        return render(request, 'home.html')

def create_client(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        country = request.POST.get('country')
        if name and country:
            Client.objects.create(name=name, country=country)
    return redirect('home')