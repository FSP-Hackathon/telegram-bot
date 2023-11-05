FROM python:3-onbuild

EXPOSE 1082

CMD ["sudo", "python", "./src/main.py"]
