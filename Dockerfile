FROM python:3.11-alpine

WORKDIR /app

COPY ./source.rinha.json /var/rinha/source.rinha.json
COPY . .

CMD ["python", "main.py"]
