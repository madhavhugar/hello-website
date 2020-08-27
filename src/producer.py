import os
import time

import requests
import schedule
from typing import TypedDict, Optional

from src.infrastructure.message_broker import MessageBroker
from src.infrastructure.db import Database


DB_URI = os.getenv('DB_URI')

KAFKA_URI = os.getenv('KAFKA_URI')
KAFKA_SSL_CAFILE_PATH = os.getenv('KAFKA_SSL_CAFILE_PATH')
KAFKA_SSL_CERTFILE_PATH = os.getenv('KAFKA_SSL_CERTFILE_PATH')
KAFKA_SSL_KEYFILE_PATH = os.getenv('KAFKA_SSL_KEYFILE_PATH')
KAFKA_UPTIME_TOPIC = os.getenv('KAFKA_UPTIME_TOPIC')

WEB_URL = os.getenv('WEB_URL')
DURATION = 2


Stat = TypedDict(
    'Stat',
    {
        'url': str,
        'status_code': int,
        'response_time': str,
        'pattern_exists': bool,
        'pattern_match': Optional[str],
     },
)


def transform_stat(
    url: str,
    res: requests.Response,
) -> Stat:
    stat = {
        'url': url,
        'status_code': res.status_code,
        'response_time': res.elapsed.total_seconds(),
        'pattern_exists': False,
        'pattern_match': 'none',
    }
    return stat


def check_status_and_publish(
    msg_broker: MessageBroker,
    url: str,
    db: Database,
) -> None:
    res = requests.get(url)
    print(f'{res=}')
    stat = transform_stat(url, res)
    print(f'{stat=}')
    msg_broker.publish(stat)


if __name__ == "__main__":
    print(f"""Starting producer which publishes stats from {WEB_URL=}...\nPublishing to {KAFKA_UPTIME_TOPIC=}""")
    db = Database(DB_URI)
    msg_broker = MessageBroker(
        topic=KAFKA_UPTIME_TOPIC,
        service_uri=KAFKA_URI,
        ssl_cafile=KAFKA_SSL_CAFILE_PATH,
        ssl_certfile=KAFKA_SSL_CERTFILE_PATH,
        ssl_keyfile=KAFKA_SSL_KEYFILE_PATH,
    )

    # Periodically check status and publish to kafka topic
    schedule.every(DURATION) \
            .seconds \
            .do(lambda: check_status_and_publish(
                            msg_broker,
                            WEB_URL,
                            db,
                        ))
    while True:
        schedule.run_pending()
        if DURATION > 1:
            time.sleep(DURATION-1)
