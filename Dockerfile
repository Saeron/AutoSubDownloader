FROM python:alpine

RUN mkdir autoSubDownloader

WORKDIR /autoSubDownloader
RUN mkdir movies tvshows

ADD main.py /autoSubDownloader
ADD requirements.txt /autoSubDownloader

RUN pip install -r requirements.txt

CMD ["python", "main.py"]