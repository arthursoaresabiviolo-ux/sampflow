from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, Http404
from django.contrib import messages
from django.utils.dateparse import parse_date
from decimal import Decimal, InvalidOperation
from io import BytesIO
from PIL import Image, UnidentifiedImageError
from .models import Client, Sample
from .invoice import generate_invoice_pdf


ALLOWED_SAMPLE_IMAGE_FORMATS = {
    'JPEG': 'image/jpeg',
    'PNG': 'image/png',
}


def read_sample_image(image_file):
    """Return verified image data and its canonical MIME type."""
    if not image_file:
        return None, None

    image_data = image_file.read()
    try:
        image = Image.open(BytesIO(image_data))
        image_format = image.format
        image.verify()
    except (UnidentifiedImageError, OSError, ValueError):
        raise ValueError('Envie uma imagem PNG ou JPEG válida.')

    mimetype = ALLOWED_SAMPLE_IMAGE_FORMATS.get(image_format)
    if not mimetype:
        raise ValueError('Envie a foto da amostra nos formatos PNG ou JPEG.')

    return image_data, mimetype


def parse_sample_weight(value): #Parses the input weight, detects the unit (kg or g), and returns a Decimal value with its unit.
    raw = (value or '').strip().lower()
    if not raw:
        return None, 'g'

    unit = 'kg' if 'k' in raw else 'g'
    normalized = raw.replace('kg', '').replace('k', '').replace('g', '').strip()

    if ',' in normalized:
        normalized = normalized.replace('.', '').replace(',', '.')

    try:
        return (Decimal(normalized) if normalized else None), unit
    except InvalidOperation:
        return None, unit


def parse_shipment_cost(value):
    """Parse a Brazilian or international currency value into a Decimal."""
    raw = (value or '').strip()
    if not raw:
        return None

    normalized = raw.replace('R$', '').replace('$', '').replace(' ', '')
    if ',' in normalized and '.' in normalized:
        if normalized.rfind(',') > normalized.rfind('.'):
            normalized = normalized.replace('.', '').replace(',', '.')
        else:
            normalized = normalized.replace(',', '')
    elif ',' in normalized:
        normalized = normalized.replace(',', '.')

    try:
        amount = Decimal(normalized).quantize(Decimal('0.01'))
        if not amount.is_finite() or amount < 0 or amount.adjusted() > 9:
            raise InvalidOperation
        return amount
    except InvalidOperation:
        raise ValueError('Informe um valor de envio válido, por exemplo: R$ 100,00.')

def home(request):
    if request.method == 'GET':
        clients = Client.objects.all().order_by('name')
        samples = Sample.objects.all().order_by('-created_at')
        dashboard_samples = list(
            Sample.objects.filter(shipping_date__isnull=False, shipment_cost__isnull=False)
            .select_related('client')
            .order_by('-shipping_date', '-id')
        )
        dashboard_costs = [
            {
                'date': sample.shipping_date.isoformat(),
                'cost': float(sample.shipment_cost),
                'client': sample.client.name,
                'contract': sample.contract_ref or 'Sem contrato',
                'courier': sample.courier or 'Não informado',
                'sample_type': sample.sample_type or 'Não informado',
            }
            for sample in dashboard_samples
        ]
        return render(request, 'home.html', {
            'clients': clients,
            'samples': samples,
            'dashboard_costs': dashboard_costs,
        })

def create_client(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address')
        country = request.POST.get('country')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        if name and country and address:
            Client.objects.create(name=name, address=address, country=country, email=email, phone=phone)
    return redirect(f"{reverse('home')}#clients-tab")

def delete_client(request, client_id):
    if request.method == 'POST':
        client = get_object_or_404(Client, id=client_id)
        client.delete()
        return redirect(f"{reverse('home')}#clients-tab")

def edit_client(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    
    if request.method == 'POST':
        client.name = request.POST.get('name')
        client.address = request.POST.get('address')
        client.country = request.POST.get('country')
        client.email = request.POST.get('email')
        client.phone = request.POST.get('phone')
        client.save()
        return redirect(f"{reverse('home')}#clients-tab")

    return redirect(f"{reverse('home')}#clients-tab")

def create_sample(request):
    if request.method == "POST":
        client_id = request.POST.get("client")
        client_instance = get_object_or_404(Client, id=client_id)
        contract_ref = request.POST.get("contract", "").strip()
        contract_month = request.POST.get("reference_month", "").strip()
        sample_type = request.POST.get("sample_type", "").strip()
        status = request.POST.get("status")
        weight, weight_unit = parse_sample_weight(request.POST.get("weight"))
        gross_weight, gross_weight_unit = parse_sample_weight(request.POST.get("gross_weight"))
        package_type = request.POST.get("package_type", "").strip()
        try:
            shipment_cost = parse_shipment_cost(request.POST.get("shipment_cost"))
        except ValueError as error:
            messages.error(request, str(error))
            return redirect(f"{reverse('home')}#samples-tab")
        fiscal_number = request.POST.get("fiscal_number", "").strip()
        shipping_date = parse_date(request.POST.get("shipping_date", ""))
        delivery_date = parse_date(request.POST.get("delivery_date", ""))
        tracking_number = request.POST.get("tracking_number", "").strip()
        courier = request.POST.get("courier", "").strip()
        screen_size = request.POST.get("screen_size", "").strip()
        cupping = request.POST.get("cupping", "").strip()
        try:
            sample_image_data, sample_image_mimetype = read_sample_image(
                request.FILES.get("sample_image")
            )
        except ValueError as error:
            messages.error(request, str(error))
            return redirect(f"{reverse('home')}#samples-tab")
        comments = request.POST.get('comments', '').strip()

        Sample.objects.create(
            client=client_instance,
            contract_ref=contract_ref,
            contract_month=contract_month,
            sample_type=sample_type,
            status=status,
            weight=weight,
            weight_unit=weight_unit,
            gross_weight=gross_weight,
            gross_weight_unit=gross_weight_unit,
            package_type=package_type,
            shipment_cost=shipment_cost,
            fiscal_number=fiscal_number,
            shipping_date=shipping_date,
            delivery_date=delivery_date,
            tracking_number=tracking_number,
            courier=courier,
            screen_size=screen_size,
            cupping=cupping,
            comments=comments,
            sample_image=sample_image_data,
            sample_image_mimetype=sample_image_mimetype
        )

        return redirect(f"{reverse('home')}#samples-tab")

    return redirect(f"{reverse('home')}#samples-tab")


def delete_sample(request, sample_id):
    if request.method == 'POST':
        sample = get_object_or_404(Sample, id=sample_id)
        sample.delete()
    return redirect(f"{reverse('home')}#samples-tab")


def edit_sample(request, sample_id):
    sample = get_object_or_404(Sample, id=sample_id)

    if request.method == 'POST':
        sample.client = get_object_or_404(Client, id=request.POST.get('client'))
        sample.contract_ref = request.POST.get('contract', '').strip()
        sample.contract_month = request.POST.get('reference_month', '').strip()
        sample.sample_type = request.POST.get('sample_type', '').strip()
        sample.status = request.POST.get('status', '').strip()
        sample.weight, sample.weight_unit = parse_sample_weight(request.POST.get('weight'))
        sample.gross_weight, sample.gross_weight_unit = parse_sample_weight(request.POST.get('gross_weight'))
        sample.package_type = request.POST.get('package_type', '').strip()
        try:
            sample.shipment_cost = parse_shipment_cost(request.POST.get('shipment_cost'))
        except ValueError as error:
            messages.error(request, str(error))
            return redirect(f"{reverse('home')}#samples-tab")
        sample.fiscal_number = request.POST.get('fiscal_number', '').strip()
        sample.shipping_date = parse_date(request.POST.get('shipping_date', ''))
        sample.delivery_date = parse_date(request.POST.get('delivery_date', ''))
        sample.tracking_number = request.POST.get('tracking_number', '').strip()
        sample.courier = request.POST.get('courier', '').strip()
        sample.screen_size = request.POST.get('screen_size', '').strip()
        sample.cupping = request.POST.get('cupping', '').strip()
        sample.comments = request.POST.get('comments', '').strip()

        if request.FILES.get('sample_image'):
            try:
                sample.sample_image, sample.sample_image_mimetype = read_sample_image(
                    request.FILES['sample_image']
                )
            except ValueError as error:
                messages.error(request, str(error))
                return redirect(f"{reverse('home')}#samples-tab")

        sample.save()

    return redirect(f"{reverse('home')}#samples-tab")


def sample_image(request, sample_id):
    sample = get_object_or_404(Sample, id=sample_id)
    if not sample.has_image:
        raise Http404("Foto não encontrada")

    data = bytes(sample.sample_image)
    response = HttpResponse(data, content_type=sample.sample_image_mimetype or 'image/jpeg')
    response['Cache-Control'] = 'public, max-age=86400'
    return response


def generate_invoice(request, sample_id):
    sample = get_object_or_404(Sample, id=sample_id)
    pdf_bytes = generate_invoice_pdf(sample)
    contract_slug = (sample.contract_ref or f"sample_{sample.id}").strip().replace('/', '_').replace(' ', '_')
    filename = f"invoice_{contract_slug}.pdf"
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="{filename}"'
    return response
