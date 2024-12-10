import paramiko
from decouple import config
import re

class AsteriskCallerID:
    def __init__(self):
        self.host = config('ASTERISK_HOST')
        self.port = config('ASTERISK_PORT', cast=int, default=22)
        self.username = config('ASTERISK_USERNAME')
        self.password = config('ASTERISK_PASSWORD')

    def _execute_command(self, command):
        try:
            print(f"Подключение к {self.host}:{self.port} с логином {self.username}...")
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(self.host, port=self.port, username=self.username, password=self.password)
            print("Соединение установлено.")

            print(f"Выполнение команды: {command}")
            stdin, stdout, stderr = client.exec_command(command)
            output = stdout.read().decode()
            error = stderr.read().decode()
            client.close()

            if error:
                print(f"Ошибка выполнения команды: {error}")
            else:
                print(f"Вывод команды: {output}")
            return output
        except Exception as e:
            print(f"Ошибка подключения: {e}")
            return None

    def get_caller_id(self):
        command = "asterisk -rx 'core show channels'"
        result = self._execute_command(command)

        if result:
            print("Результат команды:")
            print(result)

            # Ищем номер звонящего в колонке Location
            for line in result.splitlines():
                print(f"Обрабатываем строку: {line}")
                match = re.search(r'(\d+)@from-internal', line)
                if match:
                    caller_id = match.group(1)
                    print(f"Номер звонящего: {caller_id}")
                    return caller_id
            print("Caller ID не найден.")
        else:
            print("Не удалось получить информацию о звонках.")
        return None


# Пример использования
if __name__ == "__main__":
    asterisk_caller = AsteriskCallerID()
    caller_id = asterisk_caller.get_caller_id()
    if caller_id:
        print(f"Звонящий: {caller_id}")
    else:
        print("Нет активных звонков.")
