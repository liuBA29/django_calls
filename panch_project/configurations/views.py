
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

    # including client images if available
    for client in clients:
        client.image_url = client.image.url if client.image else None

    context = {
        'is_connected': is_connected,
        'is_active_call': is_active_call,
        'calling_number': calling_number,
        'clients': clients,
    }
    return render(request, 'configurations/home.html', context)




def client_list(request):
    calling_number = get_calling_number()
    is_connected = get_asterisk_connection_status()
    is_active_call = get_active_calls()
    clients = Client.objects.all()
    for client in clients:
        client.image_url = client.image.url if client.image else None

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
        'clients': clients,
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
        'clients':clients,
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
        'clients': clients,
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
        'clients': clients,
    }
    return render(request, 'configurations/call_list.html', context)



#==================call_status wiwth js script==================


def get_call_status(request):
    calling_number = get_calling_number()

    # Если calling_number является списком и он не пустой, берем первый элемент
    if isinstance(calling_number, list) and calling_number:
        calling_number = calling_number[0]
    else:
        calling_number = None  # Если список пустой, устанавливаем calling_number как None

    # Проверяем, если номер начинается с "+", удаляем его
    if isinstance(calling_number, str) and calling_number.startswith('+'):
        calling_number = calling_number[1:]

    print(f"Полученный номер звонящего: {calling_number}")  # Выводим номер для отладки

    # Поиск клиента по номеру телефона
    client = Client.objects.filter(contact_info__phone=calling_number).first()
    print(f"Найден клиент: {client.name if client else 'Не найден'}")  # Выводим имя клиента для отладки

    is_active_call = bool(calling_number)

    response_data = {
        'is_active_call': is_active_call,  # или ваша логика
        'calling_number': calling_number,
        'client_name': client.name if client else None,
        'client_image': client.image.url if client and client.image else None,  # Include the image URL
    }

    return JsonResponse(response_data)


def call_status_page(request):
    return render(request, 'configurations/get_call_status.html')



def random_number_page(request):
    context= {
        'text': "hello_world",
    }
    return render(request, 'configurations/random_number.html', context)

def active_calls_page(request):
    context= {
        'text': "hello_world",
    }
    return render(request, 'configurations/active_calls.html', context)


