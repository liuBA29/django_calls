from django.db import models
from django.utils import timezone



class ContactInfo(models.Model):
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Phone: {self.phone}, Email: {self.email}"

class Client(models.Model):
    name = models.CharField(max_length=55)
    contact_info = models.OneToOneField(ContactInfo, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to='client_images/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ClientCard(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    is_primary = models.BooleanField(default=False)  # Primary card
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Card for {self.client.name}'

class CallRecord(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True)
    channel = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    state = models.CharField(max_length=50, choices=[('active', 'Active'), ('completed', 'Completed'), ('failed', 'Failed')])
    application_data = models.TextField()
    calling_number = models.CharField(max_length=50)
    client_image = models.ImageField(upload_to='client_images/', blank=True, null=True)
    duration = models.PositiveIntegerField(null=True, blank=True)  # Duration in seconds
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.channel} - {self.state}"


