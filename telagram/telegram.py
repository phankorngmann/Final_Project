import os
import requests


def send_telegram_alert(message: str) -> bool:
    """Send a message to Telegram using BOT token and chat id from environment.

    Environment variables:
      - TELEGRAM_BOT_TOKEN: the Telegram bot token (bot<token>:...) or full token
      - TELEGRAM_CHAT_ID: the chat id or channel (e.g. @yourchannel or a numeric id)

    Returns True on HTTP 200, False otherwise.
    """
    try:
        bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
        chat_id = os.environ.get("TELEGRAM_CHAT_ID")

        if not bot_token or not chat_id:
            print("Telegram credentials not set. Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID environment variables.")
            return False

        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            'chat_id': chat_id,
            'text': message,
            'parse_mode': 'HTML'
        }

        print(f"Sending to Telegram: {url}")
        # Do not print the full message or token in production logs. This is useful for debugging.
        response = requests.post(url, data=payload, timeout=10)
        print(f"Response status: {response.status_code}")
        # Optionally: print(response.text)

        return response.status_code == 200

    except Exception as e:
        print(f"Telegram error: {e}")
        return False
