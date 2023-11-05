FROM python:latest

WORKDIR /app

COPY . .

# RUN apt update
# RUN apt-get install python3-pip -y
RUN pip3 install --upgrade setuptools 
RUN pip3 install -r requirements.txt

EXPOSE 1082

CMD ["python", "./src/main.py"]