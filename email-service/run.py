from src.main.rabbitmq_configs.consumer import RabbitMQConsumer

if __name__ == "__main__":
    consumer = RabbitMQConsumer(
        host='localhost',
        port=5672,
        username='guest',
        password='guest',
        queue='app_queue'
    )
    consumer.start()
