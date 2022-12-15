FROM python:3.9
RUN apt-get update -y
RUN apt-get install -y curl vim
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["kopf", "run", "operator.py"]
