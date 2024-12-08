import paramiko
import re

from django.contrib import messages
from django.http import JsonResponse

from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import ClientForm

def home(request):
        return render(request, 'configurations/home.html')

def call_list(request):
    return render(request, 'configurations/call_list.html')


def client_list(request):
    clients = Client.objects.all()  # Получаем всех клиентов
    return render(request, 'configurations/client_list.html', {'clients': clients})

def add_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('client_list')
    else:
        form = ClientForm()
    return render(request, 'configurations/add_client.html', {'form':form})


def edit_client(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == "POST":
        form = ClientForm(request.POST, request.FILES, instance=client)
        if form.is_valid():
            form.save()
            return redirect('client_list')
    else:
        form=ClientForm(instance=client)
    return render(request, 'configurations/edit_client.html', {'form':form})

def delete_client(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == "POST":
        client.delete()  # Удаляем клиента
        messages.success(request, f"Client {client.name} successfully deleted.")
        return redirect('client_list')  # Перенаправляем на список клиентов
    return render(request, 'configurations/delete_client.html', {'client': client})


