
#  views.py


import paramiko
import re

from django.contrib import messages
from django.http import JsonResponse

from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import ClientForm
from configurations.scripts.asterisk_connection import  AsteriskConnection

## asterisk connection

def get_asterisk_connection_status():
    """ Функция для проверки соединения с Asterisk """
    host = "192.168.101.101"  # IP удаленного сервера Asterisk
    port = 22                  # Порт для SSH (по умолчанию 22)
    username = "root"          # Логин для SSH подключения
    password = "raspberry"     # Пароль для SSH подключения

    # Создаем экземпляр подключения
    asterisk_conn = AsteriskConnection(host, port, username, password)

    # Подключаемся к серверу Asterisk
    asterisk_conn.connect()

    # Проверяем состояние соединения
    is_connected = asterisk_conn.check_connection()
    print("is connected")

    # Закрываем соединение
    asterisk_conn.close_connection()

    return is_connected

def home(request):
    # Проверяем соединение с Asterisk
    is_connected = get_asterisk_connection_status()

    # Передаем статус соединения в контекст
    return render(request, 'configurations/home.html', {'is_connected': is_connected})

def call_list(request):
    is_connected = get_asterisk_connection_status()
    return render(request, 'configurations/call_list.html', {'is_connected': is_connected})


def client_list(request):
    is_connected = get_asterisk_connection_status()
    clients = Client.objects.all()  # Получаем всех клиентов
    return render(request, 'configurations/client_list.html', {'clients': clients, 'is_connected': is_connected}, )

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


def client_detail(request, pk):
    client = get_object_or_404(Client, pk=pk)
    return render(request, 'configurations/client_detail.html', {'client': client})

