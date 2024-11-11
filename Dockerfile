# Используем официальный образ Python
FROM python:3.11-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файлы проекта в контейнер
COPY . /app

# Устанавливаем зависимости из файла requirements.txt
# Убедитесь, что ваш requirements.txt содержит fastapi и sqlite
RUN pip install --no-cache-dir -r requirements.txt

# Открываем порт для FastAPI (по умолчанию FastAPI работает на порту 8000)
EXPOSE 8000

# Запускаем FastAPI с uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]