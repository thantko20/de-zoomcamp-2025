from time import time
import pandas as pd
from sqlalchemy import create_engine

green_taxi_csv = './green_tripdata_2019-10.csv.gz'
# zones_csv = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv'

engine = create_engine('postgresql://postgres:password@localhost:5433/ny_taxi')
engine.connect()

df_iter = pd.read_csv(green_taxi_csv, compression='gzip', iterator=True, chunksize=100000)
df = next(df_iter)
df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)
df.head(n=0).to_sql(name='green_taxi_data', con=engine, if_exists="replace")
df.to_sql(name='green_taxi_data', con=engine, if_exists="append")
while True:
    try:
        t_start = time()
        df = next(df_iter)
        df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
        df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)
        df.to_sql(name='green_taxi_data', con=engine, if_exists="append")
        t_end = time()
        print("inserted chunk, took %.3f second" % (t_end - t_start))
    except StopIteration:
        break

