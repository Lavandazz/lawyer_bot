# Используем официальный образ Python
FROM python:3.13.5-slim-bookworm

# Устанавливаем временную зону
ENV TZ=Europe/Moscow
RUN apt-get update && apt-get install -y tzdata && \
    ln -fs /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo $TZ > /etc/timezone && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* \

# Устанавливаем зависимости
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код бота
COPY . .

# Запускаем приложение бота
CMD ["python", "main.py"]
