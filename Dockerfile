FROM python:3.9.19-alpine

WORKDIR /obopy
COPY requirements.txt requirements.txt
RUN apt-get update
RUN apt-get install -y gcc
# RUN apt-get install libportaudio2
RUN apt-get install -y libjack-jackd2-dev portaudio19-dev
RUN pip3 install -r requirements.txt

# copy python project files from local to /hello-py image working directory
COPY . .

# run the flask server  
# CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
CMD [ "python3", "m2.py"]