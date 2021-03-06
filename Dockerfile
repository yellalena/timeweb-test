FROM python:3.7-slim-buster

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY . /app

# ENTRYPOINT ["python", "app.py"]