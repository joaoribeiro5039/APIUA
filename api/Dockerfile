FROM python:3-alpine

RUN pip install --upgrade pip
RUN pip install opcua
RUN pip install uvicorn[standard]
RUN pip install fastapi[all]
RUN pip install redis

RUN mkdir /api

WORKDIR /usr/src/api

COPY api.py .

EXPOSE 8000
EXPOSE 4840
EXPOSE 6379

CMD ["uvicorn","api:app","--host","0.0.0.0"]