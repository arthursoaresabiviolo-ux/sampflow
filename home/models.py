from django.db import models

class Client(models.Model):
    
    name = models.CharField(max_length=150)
    country = models.CharField(max_length=150)
    address = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name