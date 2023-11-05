FROM python:3

COPY . .

RUN pip install -r requirements.txt

EXPOSE 1082

CMD ["python", "./src/main.py"]