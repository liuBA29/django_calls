import paramiko
from configurations.models import *
def get_call_records():
    try:
        # Подключение к Asterisk через SSH
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect('192.168.101.101', username='root', password='raspberry')

        # Выполнение команды Asterisk
        stdin, stdout, stderr = ssh.exec_command('asterisk -rx "core show channels verbose"')
        cdr_output = stdout.read().decode()
        error_output = stderr.read().decode()

        ssh.close()

        # Проверка на ошибки
        if error_output:
            print("Ошибка:", error_output)
            return [], error_output

        call_records = []

        # Парсинг данных из Asterisk
        for line in cdr_output.split('\n')[2:]:  # Пропускаем заголовки
            parts = line.split()
            if len(parts) > 3:  # Убедимся, что строка валидна
                application_data = ' '.join(parts[7:8])  # Собираем данные
                calling_number = extract_calling_number(application_data)  # Извлекаем номер телефона

                # Ищем клиента с указанным номером
                client = Client.objects.filter(phone=calling_number).first()

                call_records.append({
                    'channel': parts[0],
                    'location': parts[1],
                    'state': parts[2],
                    'calling_number': calling_number,
                    'client_name': client.name if client else f"Неизвестный номер ({calling_number})",
                    'client_email': client.email if client else None,
                    'client_image': client.image.url if client and client.image else None,
                })

        return call_records, None

    except Exception as e:
        # Обработка ошибок
        return [], f"Не удалось подключиться к Asterisk: {str(e)}"

        return [], "Не удалось подключиться к Астериск: " + str(e)
