FROM python:3-alpine

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN mkdir /api

WORKDIR /usr/src/api

COPY api.py .
EXPOSE 8000
EXPOSE 4840

CMD ["uvicorn","api:app","--host","0.0.0.0"]