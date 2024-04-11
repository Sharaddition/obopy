FROM python:3.9.19-alpine
WORKDIR /obopy
RUN apt-get install -y gcc
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
CMD [ "python3", "t4.py"]