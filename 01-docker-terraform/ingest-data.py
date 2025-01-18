#!/usr/bin/env python
# coding: utf-8

from time import time
import pandas as pd
import argparse
from sqlalchemy import create_engine
import os

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url
    csv_name = url.split('/')[-1]
    os.system(f'wget {url} -O {csv_name}')

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    engine.connect()

    df = pd.read_csv(csv_name, nrows=100)

    # In the Video, when Alexy read CSV, `tpep_pickup_datetime` is TEXT.
    # So, he uses `df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)` to
    # transform into `TIMESTAMP`.
    # 
    # > Update: I just transformed the parquet file into CSV and use that file just to make sure I'm following the video correctly.
    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    # Outputs `SQL` script to create the table with given connection.
    print(pd.io.sql.get_schema(df, name=table_name, con=engine))


    # Chunk the size of the data to be inserted into the database.
    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000)

    df = next(df_iter)

    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    # create the table first 
    df.head(n=0).to_sql(name=table_name, con=engine, if_exists="replace")

    # Inserting data chunk by chunk until python raises an error.
    while True:
        t_start = time()
        df = next(df_iter)
        df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
        df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
        df.to_sql(name="yellow_taxi_data", con=engine, if_exists="append")

        t_end = time()

        print("inserted chunk, took %.3f second" % (t_end - t_start))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest data into postgres')

    # user, password, host, port, database name, table name,
    # url of the csv
    parser.add_argument('--user', help='user name for postgres')
    parser.add_argument('--password', help='password for postgres')
    parser.add_argument('--host', help='host for postgres')
    parser.add_argument('--port', help='port for postgres')
    parser.add_argument('--db', help='database name for postgres')
    parser.add_argument('--table-name', help='name of the table to write the data')
    parser.add_argument('--url', help='url of the csv file')

    args = parser.parse_args()

    main(args)






