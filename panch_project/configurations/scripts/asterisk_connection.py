import paramiko

class AsteriskConnection:
    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.client = None
        self.ssh = None

    def connect(self):
        try:
            # Создаем SSH клиент
            self.client = paramiko.SSHClient()
            # Разрешаем подключение к незарегистрированным хостам (для удобства, но это нужно делать с осторожностью)
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            # Подключаемся к серверу
            self.client.connect(self.host, port=self.port, username=self.username, password=self.password)
            print("SSH connection to Asterisk server successful!")
        except Exception as e:
            print(f"Error connecting to Asterisk: {e}")
            self.client = None

    def check_connection(self):
        """ Проверка состояния соединения с Asterisk через SSH """
        if self.client:
            try:
                # Выполняем команду на сервере для проверки соединения, например, запустим команду 'asterisk -rx "core show version"'
                stdin, stdout, stderr = self.client.exec_command('asterisk -rx "core show version"')
                output = stdout.read().decode()
                if output:
                    print(f"Asterisk version:\n{output}")
                    return True
                else:
                    print("No output received from Asterisk.")
            except Exception as e:
                print(f"Error during command execution: {e}")
        return False

    def close_connection(self):
        if self.client:
            self.client.close()
            print("Disconnected from Asterisk.")

# Пример использования
if __name__ == "__main__":
    # Параметры подключения (их нужно настроить согласно вашему Asterisk серверу)
    host = "192.168.101.101"  # IP удаленного сервера Asterisk
    port = 22                  # Порт для SSH (по умолчанию 22)
    username = "root"          # Логин для SSH подключения
    password = "raspberry"      # Пароль для SSH подключения

    # Создаем экземпляр подключения
    asterisk_conn = AsteriskConnection(host, port, username, password)

    # Подключаемся к серверу Asterisk
    asterisk_conn.connect()

    # Проверяем состояние соединения
    if asterisk_conn.check_connection():
        print("Asterisk is connected.")
    else:
        print("Asterisk connection failed.")

    # Закрываем соединение
    asterisk_conn.close_connection()