
#  views.py

from decouple import config
import paramiko
import re
from django.conf import settings

from django.contrib import messages
from django.http import JsonResponse

from django.shortcuts import render, redirect, get_object_or_404
from configurations.models import *
from .forms import ClientForm
from configurations.scripts.asterisk_connection import  AsteriskConnection
from configurations.scripts.active_calls import AsteriskCalls
from configurations.scripts.calling_number import CallingNumber

## asterisk connection
host = config('ASTERISK_HOST')  # IP-адрес сервера
port = config('ASTERISK_PORT', cast=int, default=22)  # Порт SSH (по умолчанию 22)
username = config('ASTERISK_USERNAME')  # Имя пользователя для подключения
password = config('ASTERISK_PASSWORD')  # Пароль для подключения

def get_calling_number():
    calling_number = CallingNumber(host, port, username, password)
    return calling_number.get_asterisk_call_info()

def get_active_calls():
    is_active_call = AsteriskCalls()
    return is_active_call.check_active_calls()

def get_asterisk_connection_status():
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

#=========================================================================
# общие переменные


#  отсюда функции отображений
def home(request):
    calling_number = get_calling_number()
    is_connected = get_asterisk_connection_status()
    is_active_call = get_active_calls()
    clients = Client.objects.all()

    context = {
        'is_connected': is_connected,
        'is_active_call': is_active_call,
        'calling_number': calling_number,
    }
    return render(request, 'configurations/home.html', context)




def client_list(request):
    calling_number = get_calling_number()
    is_connected = get_asterisk_connection_status()
    is_active_call = get_active_calls()
    clients = Client.objects.all()
    context = {
        'is_connected': is_connected,
        'is_active_call': is_active_call,
        'clients':clients,
        'calling_number':calling_number,
    }
    return render(request, 'configurations/client_list.html', context)

def add_client(request):
    is_connected = get_asterisk_connection_status()
    is_active_call = get_active_calls()
    clients = Client.objects.all()
    if request.method == 'POST':
        form = ClientForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('client_list')
    else:
        form = ClientForm()

    context = {
        'form': form,
        'is_connected': is_connected,
        'is_active_call': is_active_call,
        'clients': clients,
    }
    return render(request, 'configurations/add_client.html', context)


def edit_client(request, pk):
    is_connected = get_asterisk_connection_status()
    is_active_call = get_active_calls()
    clients = Client.objects.all()
    client = get_object_or_404(Client, pk=pk)
    if request.method == "POST":
        form = ClientForm(request.POST, request.FILES, instance=client)
        if form.is_valid():
            form.save()
            return redirect('client_list')
    else:
        form=ClientForm(instance=client)
    context = {
        'form': form,
        'is_connected': is_connected,
        'is_active_call': is_active_call,
        'client': client,
    }
    return render(request, 'configurations/edit_client.html', context)

def delete_client(request, pk):
    is_connected = get_asterisk_connection_status()
    is_active_call = get_active_calls()
    clients = Client.objects.all()
    client = get_object_or_404(Client, pk=pk)
    if request.method == "POST":
        client.delete()  # Удаляем клиента
        messages.success(request, f"Client {client.name} successfully deleted.")
        return redirect('client_list')  # Перенаправляем на список клиентов
    context = {
        'is_connected': is_connected,
        'is_active_call': is_active_call,
        'client': client,
    }
    return render(request, 'configurations/delete_client.html', context)


def client_detail(request, pk):
    is_connected = get_asterisk_connection_status()
    is_active_call = get_active_calls()
    clients = Client.objects.all()
    client = get_object_or_404(Client, pk=pk)
    context = {
        'is_connected': is_connected,
        'is_active_call': is_active_call,
        'client': client,
    }
    return render(request, 'configurations/client_detail.html', context)


#=====================звонки===============
def call_list(request):
    is_connected = get_asterisk_connection_status()
    is_active_call = get_active_calls()
    clients = Client.objects.all()
    context = {
        'is_connected': is_connected,
        'is_active_call': is_active_call,
    }
    return render(request, 'configurations/call_list.html', context)



#==================call_status wiwth js script==================
def get_call_status(request):
    is_active_call = get_active_calls()
    calling_number = get_calling_number()
    context = {
        'is_active_call': is_active_call,
        'calling_number': calling_number,
    }
    return JsonResponse(context)

