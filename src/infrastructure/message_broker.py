import json

from typing import Iterator

from kafka import KafkaConsumer
from kafka import KafkaProducer


class MessageBroker:
    def __init__(
        self,
        topic: str,
        service_uri: str,
        ssl_cafile: str,
        ssl_certfile: str,
        ssl_keyfile: str,
    ):
        self.topic = topic
        self.service_uri = service_uri

        self.producer = KafkaProducer(
            bootstrap_servers=service_uri,
            security_protocol="SSL",
            value_serializer=(lambda dictionary: json.dumps(dictionary)
                                                     .encode('utf-8')),
            ssl_cafile=ssl_cafile,
            ssl_certfile=ssl_certfile,
            ssl_keyfile=ssl_keyfile,
        )
        self.consumer = KafkaConsumer(
            topic,
            bootstrap_servers=service_uri,
            security_protocol="SSL",
            ssl_cafile=ssl_cafile,
            ssl_certfile=ssl_certfile,
            ssl_keyfile=ssl_keyfile,
        )

    def publish(self, message):
        self.producer.send(self.topic, message)

    def consume(self) -> Iterator:
        return self.consumer
