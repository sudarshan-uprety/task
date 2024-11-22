FROM python:3.8
ENV DockerHOME=/home/app/webapp

RUN mkdir -p $DockerHOME
RUN mkdir -p $DockerHOME/static

WORKDIR $DockerHOME

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . $DockerHOME
ENTRYPOINT [ "/bin/bash", "docker-entrypoint.sh" ]
