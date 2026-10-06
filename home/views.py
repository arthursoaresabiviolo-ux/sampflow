from django.shortcuts import render, redirect, get_object_or_404
from django.utils.dateparse import parse_date
from .models import Client, Sample

def home(request):
    if request.method == 'GET':
        clients = Client.objects.all()
        samples = Sample.objects.all().order_by('-created_at')
        return render(request, 'home.html', {'clients': clients, 'samples': samples})

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
        contract_ref = request.POST.get("contract", "").strip()
        contract_month = request.POST.get("reference_month", "").strip()
        sample_type = request.POST.get("sample_type", "").strip()
        status = request.POST.get("status")
        weight = request.POST.get("weight")
        shipment_cost = request.POST.get("shipment_cost", "").strip()
        fiscal_number = request.POST.get("fiscal_number", "").strip()
        shipping_date = parse_date(request.POST.get("shipping_date", ""))
        delivery_date = parse_date(request.POST.get("delivery_date", ""))
        tracking_number = request.POST.get("tracking_number", "").strip()
        courier = request.POST.get("courier", "").strip()
        screen_size = request.POST.get("screen_size", "").strip()
        cupping = request.POST.get("cupping", "").strip()
        sample_image = request.FILES.get("sample_image")
        comments = (
            f"Origem: {request.POST.get('origin', '').strip()} | "
            f"Mês de referência: {request.POST.get('reference_month', '').strip()} | "
            f"Peneira: {request.POST.get('screen_size', '').strip()}"
        )

        Sample.objects.create(
            client=client_instance,
            contract_ref=contract_ref,
            contract_month=contract_month,
            sample_type=sample_type,
            status=status,
            weight=weight,
            shipment_cost=shipment_cost,
            fiscal_number=fiscal_number,
            shipping_date=shipping_date,
            delivery_date=delivery_date,
            tracking_number=tracking_number,
            courier=courier,
            screen_size=screen_size,
            cupping=cupping,
            comments=comments,
            sample_image=sample_image
        )

        return redirect("home")

    return redirect("home")


def delete_sample(request, sample_id):
    if request.method == 'POST':
        sample = get_object_or_404(Sample, id=sample_id)
        sample.delete()
    return redirect('home')
