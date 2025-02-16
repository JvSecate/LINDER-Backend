FROM python:3.10.11

WORKDIR /Linder-backend

COPY ./src ./src
COPY requirements.txt .

RUN pip install -r requirements.txt

CMD ["python", "./src/server.py"]
