FROM python:3.9

WORKDIR /usr/srs/app

COPY requirements.txt ./

RUN pip install -r requirements.txt

CMD ["python", "manage.py", "runserver", "migrate"]