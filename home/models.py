from django.db import models

class Client(models.Model):
    
    name = models.CharField(max_length=150)
    country = models.CharField(max_length=150)
    address = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name

class Sample(models.Model):
    class SampleType(models.TextChoices):
        PRE_SHIPMENT = 'Pré embarque', 'Pré Embarque'
        SHIPMENT = 'Embarque', 'Embarque'
        COMMERCIAL_SAMPLE = 'Amostra Comercial', 'Amostra Comercial'

    class Status(models.TextChoices):
        PENDING = 'Pendente', 'Pendente'
        AWAITING_COLLECTION = 'Aguardando coleta', 'Aguardando coleta'
        IN_TRANSIT = 'Em Trânsito', 'Em Trânsito'
        COMPLETED = 'Concluído', 'Concluído'

    class Courier(models.TextChoices):
        FEDEX = 'FedEx', 'FedEx'
        CORREIOS = 'Correios', 'Correios'
        DHL = 'DHL', 'DHL'
        UPS = 'UPS', 'UPS'

    class Currency(models.TextChoices):
        BRL = 'BRL', 'Real brasileiro (BRL)'

    PACKAGE_TYPE_CHOICES = [
        ('FedEx Large Pak (30,48 cm x 39,37 cm)', 'FedEx Large Pak (30,48 cm x 39,37 cm)'),
        ('FedEx Small Box (31,12 cm x 27,69 cm x 3,81 cm)', 'FedEx Small Box (31,12 cm x 27,69 cm x 3,81 cm)'),
        ('FedEx Medium Box (33,66 cm x 29,21 cm x 6,03 cm)', 'FedEx Medium Box (33,66 cm x 29,21 cm x 6,03 cm)'),
        ('DHL Small Flyer (40 cm x 30 cm)', 'DHL Small Flyer (40 cm x 30 cm)'),
        ('UPS Pak (40,6 cm x 33 cm x 2,5 cm)', 'UPS Pak (40,6 cm x 33 cm x 2,5 cm)'),
        ('Outro', 'Outro'),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='samples')
    contract_ref = models.CharField(max_length=100, blank=True, null=True)
    contract_month = models.CharField(max_length=100, blank=True, null=True)
    sample_type = models.CharField(max_length=100, choices=SampleType, blank=True, null=True)
    status = models.CharField(max_length=100, choices=Status, blank=True, null=True)
    weight = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    gross_weight = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    weight_unit = models.CharField(max_length=5, choices=[('g', 'g'), ('kg', 'kg')], default='g')
    gross_weight_unit = models.CharField(max_length=5, choices=[('g', 'g'), ('kg', 'kg')], default='g')
    package_type = models.CharField(max_length=100, choices=PACKAGE_TYPE_CHOICES, blank=True, null=True)
    fiscal_number = models.CharField(max_length=100, blank=True, null=True)
    shipping_date = models.DateField(blank=True, null=True)
    delivery_date = models.DateField(blank=True, null=True)
    tracking_number = models.CharField(max_length=100, blank=True, null=True)
    courier = models.CharField(max_length=100, choices=Courier, blank=True, null=True)
    screen_size = models.CharField(max_length=100, blank=True, null=True)
    cupping = models.CharField(max_length=100, blank=True, null=True)
    shipment_cost = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    shipment_currency = models.CharField(max_length=3, choices=Currency, default=Currency.BRL)
    comments = models.TextField(blank=True, null=True)
    sample_image = models.BinaryField(blank=True, null=True)
    sample_image_mimetype = models.CharField(max_length=50, blank=True, null=True, default='image/jpeg')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['shipping_date']),
            models.Index(fields=['delivery_date']),
            models.Index(fields=['status']),
            models.Index(fields=['courier']),
            models.Index(fields=['client', 'shipping_date']),
        ]

    @property
    def weight_in_kg(self): #Returns the weight converted to kilograms (kg).
        if self.weight is None:
            return None
        return self.weight if self.weight_unit == 'kg' else self.weight / 1000

    @property
    def formatted_weight(self): #Returns the weight formatted with a space before the unit.
        if self.weight is None:
            return ""
        val = f"{self.weight:.2f}".rstrip('0').rstrip('.')
        return f"{val} {self.weight_unit}"

    @property
    def weight_input_value(self): #Returns the weight formatted for input fields, without a space before the unit.
        if self.weight is None:
            return ""
        val = f"{self.weight:.2f}".rstrip('0').rstrip('.')
        return f"{val}{self.weight_unit}"

    @property
    def gross_weight_in_kg(self): #Returns the gross weight converted to kilograms (kg).
        if self.gross_weight is None:
            return None
        return self.gross_weight if self.gross_weight_unit == 'kg' else self.gross_weight / 1000

    @property
    def formatted_gross_weight(self): #Returns the gross weight formatted with a space before the unit.
        if self.gross_weight is None:
            return ""
        val = f"{self.gross_weight:.2f}".rstrip('0').rstrip('.')
        return f"{val} {self.gross_weight_unit}"

    @property
    def gross_weight_input_value(self): #Returns the gross weight formatted for input fields, without a space before the unit.
        if self.gross_weight is None:
            return ""
        val = f"{self.gross_weight:.2f}".rstrip('0').rstrip('.')
        return f"{val}{self.gross_weight_unit}"

    @property
    def has_image(self):
        if not self.sample_image:
            return False
        data = bytes(self.sample_image)
        return len(data) > 60 and not data.startswith(b'sample_images/')

    @property
    def image_data_uri(self):
        if not self.has_image:
            return ""
        import base64
        data = bytes(self.sample_image)
        encoded = base64.b64encode(data).decode('utf-8')
        mime = self.sample_image_mimetype or 'image/jpeg'
        return f"data:{mime};base64,{encoded}"

    def __str__(self):
        return self.contract_ref or f"Sample {self.pk}"
