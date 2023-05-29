FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

ADD api api
RUN mkdir -p config
COPY config/docker.cfg config/
COPY settings.yaml .

EXPOSE 5000

ENV PYTHONPATH=/app
ENV APP_SETTINGS=../config/docker.cfg

CMD ["python3", "api/app.py"]