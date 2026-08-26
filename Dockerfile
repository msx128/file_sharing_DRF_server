# syntax=docker/dockerfile:1

FROM python:3.14.6

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN python manage.py migrate

COPY . .
EXPOSE 8000

RUN useradd app
USER app

# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
