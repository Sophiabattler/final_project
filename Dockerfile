FROM ubuntu:latest
FROM python:3.9

WORKDIR /final_project

COPY . .

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update -y && apt-get install -y kmod kbd

RUN pip3 install -r requirements.txt

ENV LANG=en_US.UTF-8
CMD ["python", "final_task/initialization.py"]