# Module 1: Containerization and Infrastructure as Code

## Introduction to Docker

Docker packages software into containers. Containers are isolated from one another.

Example, packaging a data pipeline. Suppose we have a data pipeline that takes a CSV file which is run through python script and
inserted into a table in Postgres database.
This is a container. Containers are reside on host machine (windows, linux, or mac)

```
Ubuntu 20.04

Data Pipelin
- Python 3.9
- Pandas
- PG Connection Library
```

Many containers can be run on a single host machine. We can install Postgres container on the host machine and run it. Host's DB and DB on container are isolated from each other. There can also be multiple db instances running.

**Docker Image** is a snapshot of a container. This image can be run in different environments. For example, image from our own machine can be
run on Google Cloud (k8s). It will be the same container.

Docker provides -

- Reproducibility
- Local experiments
- Integration tests
- Running pipelines on the cloud
- Spark
- Serverless

Do something stupid in the container, host machine will not be affected.

This CMD runs python v3.9 in iteractive mode. `-it` flags indicates that we want to run the container in interactive mode.

```bash
docker run -it python:3.9
```

`--entrypoint` is what exactly executes when we run the container.

```bash
docker run -it --entrypoint=bash python:3.9
```

Every changes you do in the container while running it will not be saved. When the container is stopped, it goes back to default state.

In order to build image from Docker file, use -

```base
docker build -t <image:tag> .
```

[Dockerfile](./Dockerfile)
[pipeline.py](./pipeline.py)

`-t` stands for tag. `.` is the path of the directory where the Dockerfile is located.

Paramterize the pipeline script by adding args after docker run cmd.

`docker run -it test:pandas <arg-1> <arg-2>`

## Ingesting NY Taxi Data to Postgres

use `-e` to set environment variables.

Volume is a way to map a folder from the host to that in the container. For instance, since PG is a database, it needs to persist data. It will specifically
store records to the specified volume if we are using `volumes`.

We use `-v` flag to mount a volume.

`<host-path>:<container-path>`

Regarding `host-path`, on Windows, we need to write absolute path like this
`C:\\Users\TKZ\...`.
On Linux & MacOS, we can use relative path.
Or prefix with `$(pwd)` to use current directory (linux & macOS).

In order to access the database from the host machine, we need to map the port to the port on the host machine.
We use `-p` flag to map the port.

`<host-port>:<container-port>`

```bash
docker run -it \
  -e POSTGRES_USER="postgres" \
  -e POSTGRES_PASSWORD="password" \
  -e POSTGRES_DB="ny_taxi" \
  -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \
  -p 5433:5432 \
  postgres:13
```

Alexy uses `pgcli` tool to connect and interact with the Postgres database.
We can install pgcli using pip. `pip install pgcli`.
In my machine, I had to run `pip3 install pgcli --break-system-packages` to install it.

I also had to install jupyter notebook using `pip3 install jupyter --break-system-packages`.
Run `jupyter notebook` to start jupyter notebook.

ny taxi data is available [here](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)
[yellow trip data dictionary](https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf)

`pandas` lib is a convenient way to deal with tabular data like CSV.

In the video, Alexy uses `pd.read_csv("yellow_tripdata_2022-01.csv", nrows=100)` to read the CSV file. However, in my case,
I had `.parquet` file so I had to use `pd.read_parquet("yellow_tripdata_2024-01.parquet")`.

Alexy used `pd.to_datetime(df.tpep_pickup_datetime)` to convert the date column to datetime format. But I did not have to do that
because when I run `pd.io.get_schema(df, name="yellow_tripdata_2024-01.parquet")`, I get the correct `TIMESTAMP` data type.

The rest of the code that takes the data from the CSV file and inserts
it into the database is in the [Upload Data.ipynb](./Upload%20Data.ipynb) notebook.

## Connecting pgAdmin and Postgres

I already have _pgAdmin_ installed on my machine. No need to run it through docker. But here's the command anyway.

```bash
docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="password" \
  -p 5050:80 \
  dpage/pgadmin4
```

If I were to run pgAdmin inside a container, I would not be able to access the database from another container.
To be able to connect, we need to link them somehow. _They should be in one network_.

```bash
# create a network
docker network create pg-network

# then use the network while running the containers
docker run -it \
  # specify the network
  --network=pg-network \
  # specify the name
  --name
  ...
```
