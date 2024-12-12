import os
import django

# Установите переменную окружения
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_calls.settings')

# Инициализация Django
django.setup()

# Ваш код для работы с моделями
from configurations.models import Client

client = Client.objects.filter(name="Любовь").first()
if client:
    print(f"Клиент найден: {client}")
else:
    print("Клиент с именем 'Любовь' не найден")
