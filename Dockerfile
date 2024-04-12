FROM python:3.9.13-slim-buster
WORKDIR /obopy
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
EXPOSE 6969
CMD [ "python3", "t4.py"]