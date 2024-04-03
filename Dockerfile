FROM python:3.9.13-slim-buster

# WORKDIR /hello-py
# COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# copy python project files from local to /hello-py image working directory
# COPY . .

# run the flask server  
# CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
CMD [ "python3", "m1.py"]