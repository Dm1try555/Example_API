FROM python:3.9-slim

# Встановлення залежностей для роботи з MySQL
RUN apt-get update && apt-get install -y \
    build-essential \
    libmariadb-dev \
    pkg-config \
    libssl-dev \
    libffi-dev \
    python3-dev

# Встановлюємо робочий каталог
WORKDIR /app

# Копіюємо requirements.txt до контейнера
COPY requirements.txt /app/

# Встановлюємо Python-бібліотеки
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо решту файлів у контейнер
COPY . /app/

# Відкриваємо порт 8000
EXPOSE 8000

# Команда для запуску сервера Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
