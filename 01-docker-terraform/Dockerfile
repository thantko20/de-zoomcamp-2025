FROM python:3.9

RUN pip install pandas

# working directory of our container
WORKDIR /app

COPY pipeline.py pipeline.py

ENTRYPOINT [ "python", "pipeline.py" ]