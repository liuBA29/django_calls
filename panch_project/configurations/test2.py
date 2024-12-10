import paramiko
from decouple import config


def get_asterisk_call_info():
    # Устанавливаем соединение с сервером Asterisk
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, username=username, password=password)

    # Выполняем команду для получения информации о текущих звонках
    stdin, stdout, stderr = client.exec_command('asterisk -rx "core show calls"')

    # Читаем результат
    call_info = stdout.read().decode()

    # Выводим информацию о звонке в терминале
    print(call_info)

    # Закрытие подключения
    client.close()

host = config('ASTERISK_HOST')  # IP-адрес сервера
port = config('ASTERISK_PORT')  # Порт SSH (по умолчанию 22)
username = config('ASTERISK_USERNAME')  # Имя пользователя для подключения
password = config('ASTERISK_PASSWORD')  # Пароль для подключения

# Вызов функции для получения информации о звонке
get_asterisk_call_info()

