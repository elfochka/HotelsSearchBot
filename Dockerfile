FROM python:3.11.1-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

#COPY . .
COPY api /app/api
COPY config_data /app/config_data
COPY database /app/database
COPY games /app/games
COPY handlers /app/handlers
COPY hotlog /app/hotlog
COPY keyboards /app/keyboards
COPY states /app/states
COPY utils /app/utils
COPY keys.py loader.py main.py /app/

# Сначала запускаем файл, в котором будут записаны ключи в .env
CMD ["/bin/bash", "-c", "python3 keys.py && sleep 1 && python3 main.py"]
#CMD [ "python3", "main.py" ]
