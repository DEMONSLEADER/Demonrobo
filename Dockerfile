

FROM python:3.10.5-buster

WORKDIR /root/Shikimori

COPY . .

RUN pip3 install --upgrade pip setuptools

RUN pip install -U -r requirements.txt

RUN pip3 install Unidecode==1.3.6

CMD ["python3","-m","Shikimori"]
