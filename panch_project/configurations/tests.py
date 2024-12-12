import paramiko
from decouple import config


def get_calling_number():
    try:
        # Устанавливаем соединение с сервером Asterisk
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, port=port, username=username, password=password)

        # Выполняем команду для получения информации о текущих звонках
        stdin, stdout, stderr = client.exec_command('asterisk -rx "core show channels verbose"')

        # Читаем результат
        call_info = stdout.read().decode()

        # Извлекаем номера звонящих
        active_calls = extract_calling_numbers(call_info)

        # Печатаем номер для каждого активного звонка
        for call in active_calls:
            print(f"Вам звонят с номера: {call}")

    except Exception as e:
        print(f"Ошибка: {e}")

    finally:
        # Закрытие подключения
        client.close()


def extract_calling_numbers(call_info):
    calling_numbers = []

    # Разбираем строки, полученные из вывода команды
    for line in call_info.splitlines():
        # Пропускаем строку с заголовком или итоговыми данными
        if line.startswith("Channel") or "active channels" in line or "calls processed" in line:
            continue

        # Разбиваем строку по пробелам
        parts = line.split()
        if len(parts) >= 8:  # Проверяем, что строка содержит минимум 8 колонок
            caller_id = parts[7]  # Поле CallerID
            if caller_id.isdigit():  # Проверяем, что это действительно номер
                calling_numbers.append(caller_id)

    return calling_numbers


# Параметры подключения
host = config('ASTERISK_HOST')  # IP-адрес сервера
port = int(config('ASTERISK_PORT'))  # Порт SSH (по умолчанию 22)
username = config('ASTERISK_USERNAME')  # Имя пользователя для подключения
password = config('ASTERISK_PASSWORD')  # Пароль для подключения

# Вызов функции для получения информации о звонках
get_calling_number()

