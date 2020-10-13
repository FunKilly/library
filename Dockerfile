FROM python:3.8.2-slim
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN mkdir /app && \
    apt-get update
RUN apt-get install build-essential python -y
WORKDIR /app
RUN pip install pip-tools
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY . /app/

CMD gunicorn library.wsgi:application --bind 0.0.0.0:$PORT
