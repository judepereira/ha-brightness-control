FROM python:3.11-slim-bookworm

RUN         mkdir /app
WORKDIR     /app
ADD         requirements.txt .
RUN         pip install -r requirements.txt
ADD         main.py .

CMD         python main.py
