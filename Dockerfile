FROM python:3-alpine

COPY ./requirements.txt /requirements.txt
RUN pip install --upgrade pip
RUN pip install "uvicorn[standard]"
RUN pip install "fastapi[all]"
RUN mkdir /api
WORKDIR /usr/src/api
COPY ./api .
EXPOSE 8000
CMD ["uvicorn","api:app","--host","127.0.0.2","--port","8000"]