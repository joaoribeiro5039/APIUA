FROM python:3-alpine

RUN pip install --upgrade pip
RUN pip install opcua

RUN mkdir /opcserver

WORKDIR /usr/src/opcserver
COPY opcuaserver.py .
COPY nodes.json .
EXPOSE 4840

CMD ["python","opcuaserver.py","--host","0.0.0.0"]