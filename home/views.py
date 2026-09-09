from django.http import request
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

def create_sample(request):
    if request.method == "POST":
        client_id = request.POST.get("client")
        client_instance = get_object_or_404(Client, id=client_id)
        contract_ref = request.POST.get("contract_ref")
        sample_type = request.POST.get("type")
        status = request.POST.get("status")
        weight = request.POST.get("weight")
        shipment_cust = request.POST.get("shipment_cust")
        shipment_date = request.POST.get("shipment_date")
        shipment_delivery = request.POST.get("shipment_delivery")
        tracking_number = request.POST.get("tracking_number")
        correir = request.POST.get("correir")
        comments = request.POST.get("comments")
        sample_image = request.FILES.get("sample_image")

        Sample.objects.create(
            contract_ref=contract_ref,
            client=client_instance,
            type=sample_type,
            status=status,
            weight=weight,
            shipment_cust=shipment_cust,
            shipment_date=shipment_date,
            shipment_delivery=shipment_delivery,
            tracking_number=tracking_number,
            sample_image=sample_image,
            correir=correir,
            comments=comments,
        )

        return redirect("home")

    return redirect("home")