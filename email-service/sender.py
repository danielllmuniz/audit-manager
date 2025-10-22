import requests

def send_telegram_message(token, chat_id, message):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message
    }
    response = requests.post(url, data=payload)
    return response.json()

token = "8468241893:AAHKMvATtACUukm7LgTIjis5MGtdLqKzBsE"
chat_id = "-4862639025"
message = "Hello from the email service!"

send_telegram_message(token, chat_id, message)
