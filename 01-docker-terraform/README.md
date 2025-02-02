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
  --network=pg-network \
  --name postgres-db \
  -e POSTGRES_USER="postgres" \
  -e POSTGRES_PASSWORD="password" \
  -e POSTGRES_DB="ny_taxi" \
  -v /home/thantko/postgres_data:/var/lib/postgresql/data \
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
it into the database is in the [Upload Data.ipynb](./upload-data.ipynb) notebook.

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

While establishing the communication between the containers, specify the network. I do not need to connect to the port exposed
to the host machine. I need to use the internal port of the container. For example, for `5433:5432`, i need to use `5432` as the port.

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

## Putting Ingestion Script into Docker

Convert Jupyter Notebook into a Python script

```base
jupyter nbconvert --to=script upload-data.ipynb
```

`argparse` library to parse cli arguments like db user, pw, host, .csv path, etc.

use `__main__` to run the script.

yellow taxi data 2021 - https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz

Command to execute [ingest-data.py](./ingest-data.py)

```bash
URL=https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz
python3 ingest-data.py \
  --user=postgres \
  --password=password \
  --host=localhost \
  --port=5433 \
  --db=ny_taxi \
  --table-name=yellow_taxi_trips \
  --url=$URL
```

And dockerize the script!

Updated docker command to run the container. [Dockerfile](./Dockerfile)

```bash
docker build -t taxi_ingest:v001 .

URL=https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz
docker run -it \
  --network=pg-network \
  taxi_ingest:v001 \
  --user=postgres \
  --password=password \
  --host=postgres-db \
  --port=5432 \
  --db=ny_taxi \
  --table-name=yellow_taxi_trips \
  --url=$URL
```

The `run` command also has to be run within a network because pg from another container is not accessible from
`taxi_ingest` container. So, I run both pg container and `taxi_ingest` container within `pg-network`.

## Running Postgres and pgAdmin with Docker-Compose

Instead of running separate commands to run different containers, we can define them in a YAML file called `docker-compose.yml`.

[docker-compose.yml](./docker-compose.yml)

`docker compose up -d` to run the containers. `-d` = detach mode (from terminal; running in the background)

`docker compose down` to shut them down.

## SQL Refresher

Aleady knew some of the basics of SQL :D.

## Introduction to GCP

Cloud computing services offered by Google. Compute, storage..

We are going to use **Big Data**.

## Terraform

literal definition - the process of creating conditions where life can survive
software def - taking platforms like AWS, and GCP and set up infra

From Hashicorp - https://developer.hashicorp.com/terraform/intro

> HashiCorp Terraform is an **infrastructure as code** tool that lets you define both cloud and on-prem resources in human-readable configuration files
> that you can version, reuse, and share. You can then use a consistent workflow to provision and manage all of your infrastructure throughout its lifecycle.
> Terraform can manage low-level components like compute, storage, and networking resources,
> as well as high-level components like DNS entries and SaaS features.

why?

- All in one place infra;it's simple
- collaboration eg push code to gh
- reproducibility
- ensure resources are removed; prevent being charged from resources that you do not use

Key terraform commands -

- init
- plan
- apply
- destroy

![terraform commands](key-terraform-commands.png)

Service account to be used by program. Assign roles to service accounts. Keys must be **private**!
