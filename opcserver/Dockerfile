FROM python:3-alpine

RUN pip install --upgrade pip
RUN pip install opcua
RUN pip install redis

RUN mkdir /opcserver

WORKDIR /usr/src/opcserver

COPY opcserver.py .

EXPOSE 4840
EXPOSE 6379

CMD ["python","opcserver.py"]