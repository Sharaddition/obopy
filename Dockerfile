FROM python:3.9.19-alpine
WORKDIR /obopy
COPY requirements.txt requirements.txt
RUN apt-get update
RUN pip3 install -r requirements.txt
COPY . .
CMD [ "python3", "t4.py"]