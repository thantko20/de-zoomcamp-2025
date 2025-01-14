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
