FROM python:3

RUN pip install -r requirements.txt

COPY . .
EXPOSE 1082

CMD ["python", "./src/main.py"]