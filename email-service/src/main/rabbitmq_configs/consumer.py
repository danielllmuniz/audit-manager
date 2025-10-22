import pika
from .callback import rabbitmq_callback

class RabbitMQConsumer:
    def __init__(self, host='localhost', port=5672, username='guest', password='guest', queue='app_queue'):
        self.__host = host
        self.__port = port
        self.__username = username
        self.__password = password
        self.__queue = queue
        self.__channel = self.create_channel()

    def create_channel(self):
        connection_parameters = pika.ConnectionParameters(
            host=self.__host,
            port=self.__port,
            credentials=pika.PlainCredentials(self.__username, self.__password)
        )
        channel = pika.BlockingConnection(connection_parameters).channel()
        channel.queue_declare(
            queue=self.__queue,
            durable=True
        )
        channel.basic_consume(
            queue=self.__queue,
            auto_ack=False,
            on_message_callback=rabbitmq_callback,
        )
        return channel

    def start(self):
        print("Starting RabbitMQ Consumer...")
        self.__channel.start_consuming()
