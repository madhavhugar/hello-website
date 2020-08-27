## hello-website: a website uptime tracker

A given url uptime and response time tracker. A simple application that takes in a web url and publishes the statistics to kafka topic, which is then consumed and persisted to a relational database (postresql).


## Architecture

```
Kafka Producer   => Topic => Kafka Consumer => PostgreSQL
----------------            ----------------
Collects website            Persists website
    stats                      stats
```

## Setup

The project uses python 3.8 and [Aiven](https://aiven.io/) as [DaaS](https://www.stratoscale.com/blog/dbaas/what-is-database-as-a-service/)(Database as a service).

1. Create aiven-kafka(2.6.0) and aiven-postgres(12.4) instances

2. Create a `.env` by copying `.env.example`. Using the credentials from aiven dashboard, populate the environment variables.

3. Create a python virtualenv and install requirements 
  
  ```
  pip install -r requirements.txt
  ```

4. Execute migration script for the database to create schema and tables:

  ```
  python src/migration.py
  ```

5. Start the producer

```
python src/producer.py
```

6. In a new terminal start the consumer

```
python src/consumer.py
```

## Enhancements

- Improve on mypy typings
- Unit tests for message broker module
- end to end tests
