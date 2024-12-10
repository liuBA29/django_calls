#active_calls.py


import paramiko
from decouple import config

class AsteriskCalls:
    def __init__(self):
        # Параметры подключения к серверу Asterisk
        self.host = config('ASTERISK_HOST')
        self.port = config('ASTERISK_PORT', cast=int, default=22)
        self.username = config('ASTERISK_USERNAME')
        self.password = config('ASTERISK_PASSWORD')

    # Функция для подключения к серверу и выполнения команды через SSH
    def _execute_command(self, command):
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(self.host, port=self.port, username=self.username, password=self.password)

            stdin, stdout, stderr = client.exec_command(command)
            output = stdout.read().decode()
            error = stderr.read().decode()
            client.close()

            if error:
                print(f"Ошибка выполнения команды: {error}")
            return output
        except Exception as e:
            print(f"Ошибка подключения: {e}")
            return None

    # Функция для проверки активных звонков
    def check_active_calls(self):
        command = "asterisk -rx 'core show calls'"
        result = self._execute_command(command)
        num_of_calls=0

        if result:
            # Найти строку, содержащую "active calls"
            for line in result.splitlines():

                if "active call" in line:
                    print(line)
                    num_of_calls+=1

                    if "0 active calls" in line:
                        num_of_calls=0

                    return num_of_calls
                    break  # Можно остановиться, как только нашли нужную строку
        else:
            print("Не удалось получить информацию о звонках.")


# Запуск проверки
if __name__ == "__main__":
    asterisk_calls = AsteriskCalls()
    asterisk_calls.check_active_calls()
