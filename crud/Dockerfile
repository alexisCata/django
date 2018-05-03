FROM python:3.5

RUN apt-get update && apt-get install python3-pip -y

RUN mkdir -p /usr/local/crud

COPY . /usr/local/crud

WORKDIR /usr/local/crud

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["./start.sh"]