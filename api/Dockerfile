FROM python:3-alpine

RUN pip install --upgrade pip
RUN pip install "uvicorn[standard]"
RUN pip install "fastapi[all]"
RUN mkdir /api

WORKDIR /usr/src/api
COPY .api.py .
EXPOSE 8000

CMD ["uvicorn","api:app","--host","127.0.0.1","--port","8000"]