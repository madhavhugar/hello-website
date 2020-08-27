import os
import json

from src.infrastructure.message_broker import MessageBroker
from src.infrastructure.db import Database


DB_URI = os.getenv('DB_URI')

KAFKA_URI = os.getenv('KAFKA_URI')
KAFKA_UPTIME_TOPIC = os.getenv('KAFKA_UPTIME_TOPIC')
KAFKA_SSL_CAFILE_PATH = os.getenv('KAFKA_SSL_CAFILE_PATH')
KAFKA_SSL_CERTFILE_PATH = os.getenv('KAFKA_SSL_CERTFILE_PATH')
KAFKA_SSL_KEYFILE_PATH = os.getenv('KAFKA_SSL_KEYFILE_PATH')


def consume_and_store_stat(db: Database, msg_broker: MessageBroker):
    consumer_buffer = msg_broker.consume()
    for item in consumer_buffer:
        print(f"{item=}")
        stat = json.loads(item.value)
        print(f"{stat}")
        db.insert_stat(
            url=stat['url'],
            res_time_sec=stat['response_time'],
            status_code=stat['status_code'],
            pattern_exists=False,
            pattern_match='some',
        )


if __name__ == "__main__":
    print(f"""Starting consumer listening to {KAFKA_UPTIME_TOPIC}""")
    msg_broker = MessageBroker(
        topic=KAFKA_UPTIME_TOPIC,
        service_uri=KAFKA_URI,
        ssl_cafile=KAFKA_SSL_CAFILE_PATH,
        ssl_certfile=KAFKA_SSL_CERTFILE_PATH,
        ssl_keyfile=KAFKA_SSL_KEYFILE_PATH,
        )
    db = Database(DB_URI)
    consume_and_store_stat(db, msg_broker)
