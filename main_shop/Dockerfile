FROM python:3.10-slim
WORKDIR /app

RUN apt-get update && app-get install -y \
    libpq-dev \
    gcc \
    gettext \
    vim \
    && rm -rf /var/lib/apt/lists/* \

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main_shop .

CMD ["sh", "-c", "python manage.py migrate && gunicorn django_fullshop.wsgi.application --bind 0.0.0.0:8000"]
