from src.consumer import consume_and_store_stat


class KafkaPayload:
    def __init__(self, value):
        self.value = value


class MessageBrokerMock:
    consume_invoke_count = 0

    def consume(self):
        self.consume_invoke_count += 1
        return [
            KafkaPayload(value=b'{"url": "https://stackoverflow.com", "status_code": 200, "response_time": 0.208705}'),
            KafkaPayload(value=b'{"url": "https://stackoverflow.com", "status_code": 200, "response_time": 0.208706}'),
        ]


class DatabaseMock:
    insert_stat_invoke_count = 0
    insert_stat_invoke_params = []

    def __init__(self, db_uri):
        self.db_uri = db_uri

    def insert_stat(
        self,
        url: str,
        res_time_sec: float,
        status_code: int,
        pattern_exists: bool,
        pattern_match: str,
    ):
        self.insert_stat_invoke_count += 1
        self.insert_stat_invoke_params.append((
            url,
            res_time_sec,
            status_code,
            pattern_exists,
            pattern_match,
        ))


def test_consume_and_store_stat():
    db = DatabaseMock('db_uri')
    msg_broker = MessageBrokerMock()
    consume_and_store_stat(db, msg_broker)

    assert msg_broker.consume_invoke_count == 1
    assert db.insert_stat_invoke_count == 2
    assert db.insert_stat_invoke_params[0] == ('https://stackoverflow.com', 0.208705, 200, False, 'some')
    assert db.insert_stat_invoke_params[1] == ('https://stackoverflow.com', 0.208706, 200, False, 'some')
