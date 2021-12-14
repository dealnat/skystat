FROM python:3.8-slim-buster

WORKDIR /app

RUN apt update && apt install curl python3-dev gcc libgnutls28-dev libpq-dev python3-pip python3-venv python3-wheel libcurl4-openssl-dev libssl-dev -y

COPY requirments.txt requirments.txt

RUN pip3 install -r requirments.txt

COPY . . 

CMD [ "python3", "main.py", "-t", "1650821709:AAF0OrGdGAjjRvERGUCFu7ByarMAliOX7w8", "-a", "266536993", "-d", "/app/data.db" ]
