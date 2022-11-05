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
select p.Id, p.AcceptedAnswerId, p.CreationDate, p.Title, p.Body, p.Tags, a.Body as 'Answer Body'
from Posts as p join Posts as a on p.AcceptedAnswerId = a.Id
where p.Tags like '%<cassandra>%' and p.AcceptedAnswerId is not null
order by CreationDate asc
```

Here we select all questions with a Cassandra tag and an accepted answer.
You can then download the csv.

The order is ascending so that we only have to add at the end when we update the file.