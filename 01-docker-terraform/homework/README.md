# Module 1: Homework

## Question 1

CLI Command

```bash
# first run the image
docker run -it --entrypoint=bash python:3.12.8

# then get the pip version
pip --version
# ouputs
# pip 24.3.1 from /usr/local/lib/python3.12/site-packages/pip (python 3.12)
```

**Answer** - 24.3.1

## Question 2

**Answer** - `db:5432` because docker compose creates a default network and hostnames resolve to service names. Containers can also communicate with each other using container ports.

## Question 3

### 1. Up to 1 Mile

Answer - 104802

Ingesting taxi data - [ingest.py](./ingest.py)

Solution

```sql
select count(1) from green_taxi_trips
where lpep_dropoff_datetime >= '2019-10-01'
and lpep_dropoff_datetime < '2019-11-01'
and trip_distance <= 1
```

### 2. In between 1 (exclusive) and 3 miles (inclusive)

Answer - 198924

Solution

```sql
select count(1) from green_taxi_trips
where lpep_dropoff_datetime >= '2019-10-01'
and lpep_dropoff_datetime < '2019-11-01'
and trip_distance > 1 and trip_distance <= 3
```

### 3. In between 3 (exclusive) and 7 miles (inclusive)

Answer - 109603

```sql
select count(1) from green_taxi_trips
where lpep_dropoff_datetime >= '2019-10-01'
and lpep_dropoff_datetime < '2019-11-01'
and trip_distance > 3 and trip_distance <= 7
```

### 4. In between 7 (exclusive) and 10 miles (inclusive)

Answer - 27678

```sql
select count(1) from green_taxi_trips
where lpep_dropoff_datetime >= '2019-10-01'
and lpep_dropoff_datetime < '2019-11-01'
and trip_distance > 7 and trip_distance <= 10
```

### 5. Over 10 miles

Answer - 35189

```sql
select count(1) from green_taxi_trips
where lpep_dropoff_datetime >= '2019-10-01'
and lpep_dropoff_datetime < '2019-11-01'
and trip_distance > 10
```

## Question 4

Answer - 2019-10-31

```sql
select date(lpep_pickup_datetime) as pickup_date, max(trip_distance) as max_trip_distance
from green_taxi_trips
group by pickup_date
order by max_trip_distance desc
limit 1
```

## Question 5

Answer - East Harlem North, East Harlem South, Morningside Heights

```sql
select z."Zone" as zone, SUM(gt.total_amount)
from green_taxi_trips gt
join zones z on gt."PULocationID" = z."LocationID"
where date(gt.lpep_pickup_datetime) = '2019-10-18'
group by z."Zone"
having SUM(gt.total_amount) > 13000
order by SUM(gt.total_amount) desc
```

## Question 6

Answer - JFK Airport

```sql
select
	dpz."Zone" as dropoff_zone,
	max(gt.tip_amount) as largest_tip
from green_taxi_trips gt
join zones dpz on dpz."LocationID" = gt."DOLocationID"
join zones puz on puz."LocationID" = gt."PULocationID"
where puz."Zone" = 'East Harlem North'
group by dpz."Zone"
order by largest_tip desc
limit 1
```

## Question 7
