FROM python:latest

WORKDIR /app

COPY . .


run apt update 
run apt install -y nodejs
run pip install -r /app/requirements.txt



ENV port=5000

EXPOSE 5000


CMD [ "python3", "bot.py" ]