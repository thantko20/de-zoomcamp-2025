FROM python:3.9

RUN apt install wget
RUN pip install pandas sqlalchemy psycopg2

# working directory of our container
WORKDIR /app

COPY ingest-data.py ingest-data.py

ENTRYPOINT [ "python", "ingest-data.py" ]