FROM python:3.9.13-slim-buster

WORKDIR /obopy
COPY requirements.txt requirements.txt
RUN apt-get update
RUN apt-get install -y libjack-jackd2-dev portaudio19-dev
RUN pip3 install -r requirements.txt

# copy python project files from local to /hello-py image working directory
COPY . .

# run the flask server  
# CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
CMD [ "python3", "m1.py"]