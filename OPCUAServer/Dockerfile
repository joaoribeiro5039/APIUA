FROM python:3-alpine

RUN pip install --upgrade pip
RUN pip install opcua
RUN mkdir /testopcserver
WORKDIR /usr/src/testopcserver
COPY ./OPCServer .
EXPOSE 4840/tcp
CMD ["python","opcuaserver.py"]