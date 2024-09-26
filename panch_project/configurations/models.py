from django.db import models

from django.db import models


class CallRecord(models.Model):
    channel = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    state = models.CharField(max_length=50)
    application_data = models.TextField()
    calling_number = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.channel} - {self.state}"


class Client(models.Model):
    name = models.CharField(max_length=55)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class ClientCard(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'Card for {self.client.name}'

