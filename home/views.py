from django.shortcuts import render, redirect, get_object_or_404
from .models import Client

def home(request):
    if request.method == 'GET':
        clients = Client.objects.all()
        return render(request, 'home.html', {'clients': clients})

def create_client(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address')
        country = request.POST.get('country')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        if name and country and address:
            Client.objects.create(name=name, address=address, country=country, email=email, phone=phone)
    return redirect('home')

def delete_client(request, client_id):
    if request.method == 'POST':
        client = get_object_or_404(Client, id=client_id)
        client.delete()
        return redirect('home')

def edit_client(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    
    if request.method == 'POST':
        client.name = request.POST.get('name')
        client.address = request.POST.get('address')
        client.country = request.POST.get('country')
        client.email = request.POST.get('email')
        client.phone = request.POST.get('phone')
        client.save()
        return redirect('home')

    return redirect('home')