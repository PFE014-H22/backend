# Backend

backend

## To build the docker container

```bash
docker-compose build
```

## To run the docker container

```bash
docker-compose up
```

## To query the questions from StackOverflow

Go to the StackExchange data explorer (https://data.stackexchange.com/stackoverflow/query/new) and compose a new query.

```
select Id, AcceptedAnswerId,CreationDate, Title, Body, Tags
from Posts
where Tags like '%<cassandra>%' and AcceptedAnswerId is not null
order by CreationDate desc
```

Here we select all questions with a Cassandra tag and an accepted answer.
You can then download the csv.