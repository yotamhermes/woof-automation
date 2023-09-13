FROM python:3.11

COPY app.py requirements.txt ./

RUN python3.11 -m pip install -r requirements.txt -t .

CMD ["python3.11", "app.py"]

EXPOSE 80