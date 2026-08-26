from django.shortcuts import render, redirect, get_object_or_404
from .models import Client

def home(request):
    if request.method == 'GET':
        clients = Client.objects.all()
        return render(request, 'home.html', {'clients': clients})

def create_client(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        country = request.POST.get('country')
        if name and country:
            Client.objects.create(name=name, country=country)
    return redirect('home')

def delete_client(request, client_id):
    if request.method == 'POST':
        client = get_object_or_404(Client, id=client_id)
        client.delete()
        return redirect('home')