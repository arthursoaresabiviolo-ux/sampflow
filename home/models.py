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
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='samples')
    contract_ref = models.CharField(max_length=100, blank=True, null=True)
    contract_month = models.CharField(max_length=100, blank=True, null=True)
    sample_type = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True)
    weight = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    weight_unit = models.CharField(max_length=5, choices=[('g', 'g'), ('kg', 'kg')], default='g')
    shipment_cost = models.CharField(max_length=100, blank=True, null=True)
    fiscal_number = models.CharField(max_length=100, blank=True, null=True)
    shipping_date = models.DateField(blank=True, null=True)
    delivery_date = models.DateField(blank=True, null=True)
    tracking_number = models.CharField(max_length=100, blank=True, null=True)
    courier = models.CharField(max_length=100, blank=True, null=True)
    screen_size = models.CharField(max_length=100, blank=True, null=True)
    cupping = models.CharField(max_length=100, blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    sample_image = models.ImageField(upload_to='sample_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

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

    def __str__(self):
        return self.contract_ref or f"Sample {self.pk}"