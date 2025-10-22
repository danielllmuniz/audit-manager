import json
import pika

class RabbitMQPublisher:
    def __init__(self, host='localhost', port=5672, username='guest', password='guest', exchange='app_exchange', routing_key=''):
        self.__host = host
        self.__port = port
        self.__username = username
        self.__password = password
        self.__exchange = exchange
        self.__routing_key = routing_key
        self.__channel = self.create_channel()

    def create_channel(self):
        connection_parameters = pika.ConnectionParameters(
            host=self.__host,
            port=self.__port,
            credentials=pika.PlainCredentials(self.__username, self.__password)
        )
        channel = pika.BlockingConnection(connection_parameters).channel()
        return channel

    def send_message(self, body: dict):
        self.__channel.basic_publish(
            exchange=self.__exchange,
            routing_key=self.__routing_key,
            body=json.dumps(body),
            properties=pika.BasicProperties(
                delivery_mode=2,
            )
        )

rabbit_mq_publisher = RabbitMQPublisher()
rabbit_mq_publisher.send_message({"message": "estou escrevendo do publisher!"})
