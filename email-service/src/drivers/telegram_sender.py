import requests

def send_telegram_message(
        message: str,
        token = "",
        chat_id: str = "") -> None:

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message
    }
    requests.post(url, data=payload, timeout=30)
