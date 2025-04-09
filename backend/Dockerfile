FROM python:3.12.9-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /django

RUN pip3 install --upgrade pip

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

# COPY . .

# CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]