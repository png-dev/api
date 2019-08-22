from kombu.compat import Publisher as Producer
from kombu import Connection
import os
import logging

_logger = logging.getLogger('apis')


class Publisher:
    def __init__(self):
        pass

    def establish_connection(self):
        cloudamqp_url = os.environ.get('CLOUDAMQP_URL', 'amqp://rabbitmq:rabbitmq@10.0.0.32:5672')
        return Connection(cloudamqp_url)

    def publish(self, exchange_name, routing_key, message):
        connection = self.establish_connection()
        publisher = Producer(connection=connection,
                             exchange=exchange_name,
                             routing_key=routing_key,
                             exchange_type="direct")

        publisher.send(message)
        _logger.info("Publish message {} to exchange: {} with routing key: {}  ".format(message, exchange_name, routing_key))
        publisher.close()
        connection.close()
