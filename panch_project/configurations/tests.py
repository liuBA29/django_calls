import paramiko
from decouple import config


def get_asterisk_call_info():
    try:
        # Устанавливаем соединение с сервером Asterisk
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username=username, password=password)

        # Выполняем команду для получения информации о текущих звонках
        stdin, stdout, stderr = client.exec_command('asterisk -rx "core show channels verbose"')

        # Читаем результат
        call_info = stdout.read().decode()
        error_info = stderr.read().decode()

        if error_info:
            print(f"Ошибка выполнения команды: {error_info}")
            return

        # Пример: извлекаем номера звонящих
        active_calls = extract_calling_numbers(call_info)
        if active_calls:
            print(f"Номер звонящего: {', '.join(active_calls)}")
        else:
            print("Нет активных звонков.")

    except Exception as e:
        print(f"Ошибка подключения или выполнения команды: {e}")

    finally:
        # Закрытие подключения
        client.close()


def extract_calling_numbers(call_info):
    """
    Функция для извлечения номеров звонящих из вывода команды.
    """
    calling_numbers = []

    # Разбираем строки, полученные из вывода команды
    for line in call_info.splitlines():
        if "Dial" in line:
            parts = line.split(',')
            if len(parts) > 1:
                # Извлекаем номер звонящего из части строки, которая выглядит как 'SIP/12,20,...'
                number = extract_calling_number(parts[0])
                if number:
                    calling_numbers.append(number)

    return calling_numbers


def extract_calling_number(application_data):
    """
    Функция для извлечения номера звонящего из строки.
    Пример: 'Dial(SIP/12,,HhtrIb(func-apply))'
    """
    if "SIP" in application_data:
        # Извлекаем номер звонящего из строки 'SIP/12'
        return application_data.split('/')[1]
    return None


# Параметры подключения
host = config('ASTERISK_HOST')  # IP-адрес сервера
port = config('ASTERISK_PORT')  # Порт SSH (по умолчанию 22)
username = config('ASTERISK_USERNAME')  # Имя пользователя для подключения
password = config('ASTERISK_PASSWORD')  # Пароль для подключения

# Вызов функции для получения информации о звонках
get_asterisk_call_info()
