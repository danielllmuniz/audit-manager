import requests

def send_telegram_message(
        message: str,
        token = "8468241893:AAHKMvATtACUukm7LgTIjis5MGtdLqKzBsE",
        chat_id: str = "-4862639025") -> None:

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message
    }
    requests.post(url, data=payload, timeout=30)
