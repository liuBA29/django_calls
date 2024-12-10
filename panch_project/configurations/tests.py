import paramiko
import re
from decouple import config

# Параметры подключения к серверу Asterisk
HOST = config('ASTERISK_HOST')  # IP-адрес сервера
PORT = config('ASTERISK_PORT')  # Порт SSH (по умолчанию 22)
USERNAME = "root"  # Имя пользователя для подключения
PASSWORD = "raspberry"  # Пароль для подключения


# Функция для выполнения команды на сервере Asterisk через SSH
def execute_asterisk_command(command):
    try:
        # Создаем SSH-клиент
        client = paramiko.SSHClient()

        # Автоматически добавляем ключи хоста (если они отсутствуют)
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Подключаемся к серверу Asterisk
        client.connect(HOST, port=PORT, username=USERNAME, password=PASSWORD)

        # Выполняем команду
        stdin, stdout, stderr = client.exec_command(command)

        # Получаем вывод команды
        output = stdout.read().decode()
        client.close()

        return output
    except Exception as e:
        print(f"Ошибка подключения: {e}")
        return None


# Функция для проверки наличия звонков
def check_active_calls():
    # Выполняем команду для проверки активных каналов
    command = "asterisk -rx 'core show channels'"
    result = execute_asterisk_command(command)

    if result:
        # Если результат содержит информацию о каналах, то проверим наличие звонков
        if "No active channels" in result:
            print("Нет активных звонков в данный момент.")
        else:
            print("Есть активные звонки:")
            print(result)
    else:
        print("Не удалось получить информацию о звонках.")


# Запуск проверки активных звонков
if __name__ == "__main__":
    check_active_calls()

