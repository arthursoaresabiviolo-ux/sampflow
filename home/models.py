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
    shipment_cust = models.CharField(max_length=100, blank=True, null=True)
    shipment_date = models.DateField(blank=True, null=True)
    shipment_delivery = models.CharField(max_length=100, blank=True, null=True)
    tracking_number = models.CharField(max_length=100, blank=True, null=True)
    courier = models.CharField(max_length=100, blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    sample_image = models.ImageField(upload_to='sample_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name