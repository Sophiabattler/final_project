FROM python:3.9

WORKDIR /final_project1

COPY . .

RUN pip install -r requirements.txt

ENV LANG=en_US.UTF-8
CMD ["python", "final_task/initialization.py"]