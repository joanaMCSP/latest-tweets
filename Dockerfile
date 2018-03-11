FROM python:3.6

ADD requirements.txt /app/requirements.txt

COPY src/*.py /app/

WORKDIR /app/

RUN pip install -r requirements.txt

CMD python3 /app/app.py
