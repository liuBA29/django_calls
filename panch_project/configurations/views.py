import paramiko
import re

from django.contrib import messages
from django.http import JsonResponse

from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import ClientForm


# Пример данных для разных запросов
content_list = [
    "Обновлённое содержимое страницы1",
    "Обновлённое содержимое страницы2",
    "Обновлённое содержимое страницы3",
]

current_index = 0  # Переменная для отслеживания текущего индекса


def get_dynamic_data(request):
    global current_index
    # Получаем текущий контент
    new_content = content_list[current_index]

    # Обновляем индекс для следующего запроса
    current_index = (current_index + 1) % len(content_list)  # Вернемся к 0, если достигнем конца списка

    # Возвращаем данные в формате JSON
    return JsonResponse({'new_content': new_content})


def check_incoming_calls(request):
    call_records, error_message = get_call_records()  # Get the call records from your existing function

    if error_message:
        return JsonResponse({'error': error_message}, status=500)

    # Check if there are any call records
    if call_records:
        # Get the calling number of the last call or the first one based on your logic
        calling_numbers = [record.calling_number for record in call_records if record.calling_number]
        if calling_numbers:
            return JsonResponse({'message': f'Вам звонят с номера {calling_numbers[0]}.'})

    return JsonResponse({'message': 'Нет новых звонков.'})


def get_call_records_view(request):
    call_records, error_message = get_call_records()

    if error_message:
        return JsonResponse({'error': error_message}, status=500)

    data = {
        'call_records': [
            {
                'channel': record.channel,
                'location': record.location,
                'state': record.state,
                'calling_number': record.calling_number,
            } for record in call_records
        ]
    }

    return JsonResponse(data)




def get_call_records():
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect('192.168.101.101', username='root', password='raspberry')

        stdin, stdout, stderr = ssh.exec_command('asterisk -rx "core show channels verbose"')
        cdr_output = stdout.read().decode()
        error_output = stderr.read().decode()

        ssh.close()

        if error_output:
            print("Ошибка:", error_output)
            return []

        call_records = []
        for line in cdr_output.split('\n')[2:]:  # Пропускаем первые две строки заголовков
            parts = line.split()
            if len(parts) > 3:  # Проверяем, что строка валидная
                application_data = ' '.join(parts[7:8])  # Объединяем оставшуюся часть
                calling_number = extract_calling_number(application_data)  # Извлекаем номер

                #ищем клиента с этим номером или контакт
                client = Client.objects.filter(phone=calling_number).first()
                client_image= client.image.url if client and client.image else None


                call_records.append(CallRecord(
                    channel=parts[0],
                    location=parts[1],
                    state=parts[2],
                    calling_number=application_data,
                    client_image=client_image,

                ))

        return call_records, None
    except Exception as e:
        return [], "Не удалось подключиться к Астериск:" + str(e)






def extract_calling_number(application_data):
    # Пример формата строки:
    # "Dial(SIP/12,,HhtrIb(func-apply)"
    # Нужно искать Caller ID в application_data
    if "Dial" in application_data:
        parts = application_data.split(',')
        if len(parts) > 1:
            # Пример: Caller ID может быть первым элементом
            return parts[0].split('/')[1]  # Извлекаем номер
    return None


def home(request):
        return render(request, 'configurations/home.html')

def call_list(request):
    call_records, error_message = get_call_records()

    if error_message:
        messages.error(request, error_message)

    return render(request, 'configurations/call_list.html', {
        'call_records': call_records


    })


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


def check_incoming_calls(request):
    call_records, error_message = get_call_records()  # Get the call records from your existing function

    if error_message:
        return JsonResponse({'error': error_message}, status=500)

    # Check if there are any call records
    if call_records:
        # Get the calling number of the last call
        calling_number = call_records[0].calling_number  # Assuming you want the first call record

        # Check if a client exists with the calling number
        try:
            client = Client.objects.get(phone=calling_number)
            message = f"Звонит клиент: {client.name}"
        except Client.DoesNotExist:
            message = f"Вам звонят с номера {calling_number}."

        return JsonResponse({'message': message})

    return JsonResponse({'message': 'Нет новых звонков.'})
