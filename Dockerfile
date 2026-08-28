# syntax=docker/dockerfile:1

FROM python:3.14.6

WORKDIR /app
RUN apt-get update && apt-get install -y curl
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"
RUN uv venv
COPY requirements.txt .
RUN uv pip install --no-cache-dir -r requirements.txt
# uv pip install is the correct way for sort of this tasks

COPY . .
EXPOSE 8000

RUN useradd app
USER app

CMD [".venv/bin/python", "manage.py", "runserver", "0.0.0.0:8000"]
