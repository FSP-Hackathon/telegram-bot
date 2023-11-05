FROM python:3

WORKDIR /app

COPY . .

RUN pip install --upgrade setuptools 
RUN pip install -r requirements.txt

EXPOSE 1082

CMD ["python", "./src/main.py"]