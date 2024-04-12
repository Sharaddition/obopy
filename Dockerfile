FROM python:3.9.13-slim-buster
WORKDIR /obopy
# RUN apt-get update
# RUN apt-get install -y gcc
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
CMD [ "python3", "t4.py"]