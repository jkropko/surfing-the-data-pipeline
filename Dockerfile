# syntax=docker/dockerfile:1

FROM python:3.11.4-bookworm

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

RUN apt-get update

RUN apt-get install nodejs -y

RUN apt-get install npm -y

RUN npm install -g dbdocs

WORKDIR /surfing

EXPOSE 8888
EXPOSE 8050

CMD ["jupyter", "lab", "--ip=0.0.0.0","--allow-root"]
