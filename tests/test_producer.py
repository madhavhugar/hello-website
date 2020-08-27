from src.producer import check_status_and_publish
from requests import Response


class MessageBrokerMock:
    publish_invoke_count = 0
    publish_invoke_params = []

    def publish(self, message):
        self.publish_invoke_count += 1
        self.publish_invoke_params.append(message)


class DatabaseMock:
    insert_stat_invoke_count = 0
    insert_stat_invoke_params = []

    def __init__(self, db_uri):
        self.db_uri = db_uri


class Elapsed:
    def __init__(self, seconds):
        self.seconds = seconds

    def total_seconds(self):
        return self.seconds


class ResponseMock:
    status_code = 200
    elapsed = Elapsed(0.54321)


def test_check_status_and_publish(mocker):
    url = 'https://stackoverflow.com'
    mocker.patch('requests.get', return_value=ResponseMock())

    db = DatabaseMock('db_uri')
    msg_broker = MessageBrokerMock()
    check_status_and_publish(msg_broker, url, db)

    assert msg_broker.publish_invoke_count == 1
    assert msg_broker.publish_invoke_params[0] == {
                                                    'pattern_exists': False,
                                                    'pattern_match': 'none',
                                                    'response_time': 0.54321,
                                                    'status_code': 200,
                                                    'url': 'https://stackoverflow.com'
                                                }
