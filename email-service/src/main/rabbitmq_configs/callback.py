import json
from src.drivers.telegram_sender import send_telegram_message

def rabbitmq_callback(ch, method, properties, body):
    msg = body.decode('utf-8')
    formatted_msg = json.loads(msg)
    telegram_message = formatted_msg["message"]
    send_telegram_message(telegram_message)
