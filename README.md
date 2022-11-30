# Backend

backend

## To build the docker container

```bash
docker compose build
```

## To run the docker container

```bash
docker compose up
```

## To query the questions from StackOverflow

Go to the StackExchange data explorer (https://data.stackexchange.com/stackoverflow/query/new) and compose a new query.

```sql
select p.Id, p.AcceptedAnswerId, p.CreationDate, p.Title, p.Body, p.Tags, a.Body as 'Answer Body'
from Posts as p join Posts as a on p.AcceptedAnswerId = a.Id
where p.Tags like '%<cassandra>%' and p.AcceptedAnswerId is not null
order by CreationDate asc
```

Here we select all questions with a Cassandra tag and an accepted answer.
You can then download the csv.

The order is ascending so that we only have to add at the end when we update the file.

## Available Routes

### `GET /search?q={query}&t={technology}`
List of parameters related to the query, aggregated via the parameter name and the sources that provided the answer.
```json
{
    "answers": [
        {
            "parameter": {
                "matches": 2,
                "name": "rack"
            },
            "similarity_score": 0.10795949886252758,
            "sources": [
                {
                    "answer_id": "38976606",
                    "link": "https://stackoverflow.com/a/38976606",
                    "question_body": "<p>I have a 3 node Cassandra cluster...</p>",
                    "question_id": "38973463",
                    "question_title": "How to update configuration of a Cassandra cluster",
                    "response_body": "<p>There are multiple approaches...</p>",
                    "similarity_score": 0.37685303543542165,
                    "source_name": "stackoverflow",
                    "tags": [
                        "cassandra",
                        "devops"
                    ]
                },
                ...
            ]
        },
        ...
    ],
    "query": "how to make cassandra work",
    "technology": "cassandra"
}
```

### `GET /answers/{question_id}`
Fetch all the answers associated with a stackoverflow question ID.
```json
[
    {
        "answer_id": 50461518,
        "body": "<p>We solve such issues ...</p>",
        "content_license": "CC BY-SA 4.0",
        "creation_date": 1526972016,
        "is_accepted": true,
        "last_activity_date": 1526972016,
        "link": "https://stackoverflow.com/questions/50458395/how-to-make-1-million-inserts-in-cassandra/50461518#50461518",
        "owner": {
            "accept_rate": 85,
            "account_id": 1670457,
            "display_name": "Michal",
            "link": "https://stackoverflow.com/users/1537003/michal",
            "profile_image": "https://www.gravatar.com/avatar/7781ac8717f1e343e651a91d9183eb4a?s=256&d=identicon&r=PG",
            "reputation": 1925,
            "user_id": 1537003,
            "user_type": "registered"
        },
        "question_id": 50458395,
        "score": 0
    },
    ...
]
```

### `GET /technologies`
List of all available technologies to search from
```json
[
    {
        "key": "cassandra",
        "value": "cassandra"
    }
]
```