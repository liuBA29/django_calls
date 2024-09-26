import paramiko
import re

from django.core.checks import messages
from django.http import JsonResponse

from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import ClientForm



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
                call_records.append(CallRecord(
                    channel=parts[0],
                    location=parts[1],
                    state=parts[2],
                    calling_number=application_data,

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
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('client_list')
    else:
        form = ClientForm()
    return render(request, 'configurations/add_client.html', {'form':form})


def edit_client(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == "POST":
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('client_list')
    else:
        form=ClientForm(instance=client)
    return render(request, 'configurations/edit_client.html', {'form':form})

