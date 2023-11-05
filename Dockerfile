FROM python:3

COPY . .
EXPOSE 1082

CMD ["python", "./src/main.py"]
