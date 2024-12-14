#calling_number.py

import paramiko
from decouple import config
import json


class CallingNumber:
    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    def get_asterisk_call_info(self):
        try:
            # Устанавливаем соединение с сервером Asterisk
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(self.host, port=self.port, username=self.username, password=self.password)

            # Выполняем команду для получения информации о текущих звонках
            stdin, stdout, stderr = client.exec_command('asterisk -rx "core show channels verbose"')

            # Читаем результат
            call_info = stdout.read().decode()
            error_info = stderr.read().decode()

            if error_info:
                return json.dumps({"error": f"Ошибка выполнения команды: {error_info}"}, ensure_ascii=False)

            # Извлекаем номера звонящих
            active_calls = self.extract_calling_numbers(call_info)

            # Выводим сообщение для каждого активного звонка
            for call in active_calls:
                print(f"Вам звонят с номера {call}")

            # Формируем результат в формате JSON

            return active_calls

        except Exception as e:
            # Обработка ошибки
            error_result = {
                "status": "error",
                "message": str(e)
            }
            return json.dumps(error_result, ensure_ascii=False, indent=4)

        finally:
            # Закрытие подключения
            client.close()

    def extract_calling_numbers(self, call_info):
        """
        Функция для извлечения CallerID из вывода команды.
        """
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


def extract_calling_number(application_data):
    """
    Функция для извлечения номера звонящего из строки.
    Пример: 'Dial(SIP/12,,HhtrIb(func-apply))'
    """
    if "Dial" in application_data:
        parts = application_data.split(',')
        if len(parts) > 1:
            # Извлекаем номер звонящего
            return parts[0].split('/')[1]  # Например, 'SIP/12' -> '12'
    return None


# Параметры подключения
host = config('ASTERISK_HOST')  # IP-адрес сервера
port = int(config('ASTERISK_PORT'))  # Порт SSH (по умолчанию 22)
username = config('ASTERISK_USERNAME')  # Имя пользователя для подключения
password = config('ASTERISK_PASSWORD')  # Пароль для подключения

# Создаем экземпляр класса CallingNumber
calling_number = CallingNumber(host, port, username, password)

# Вызов функции для получения информации о звонках
json_result = calling_number.get_asterisk_call_info()


