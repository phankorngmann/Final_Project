import os
import requests
import logging

logger = logging.getLogger(__name__)


def send_telegram_alert(message: str) -> bool:
    """Send a message to Telegram using BOT token and chat id from environment.

    Environment variables:
      - TELEGRAM_BOT_TOKEN: the Telegram bot token (e.g. 123456:ABC-DEF...)
      - TELEGRAM_CHAT_ID: the chat id or channel (e.g. @yourchannel or a numeric id)

    Returns True on success, False otherwise.
    """
    try:
        bot_token = (os.environ.get("TELEGRAM_BOT_TOKEN") or "").strip()
        chat_id = (os.environ.get("TELEGRAM_CHAT_ID") or "").strip()

        if not bot_token or not chat_id:
            logger.warning("Telegram credentials not set. Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID environment variables.")
            return False

        # Telegram message limit
        if len(message) > 4096:
            logger.debug("Message too long for Telegram, truncating to 4096 chars.")
            message = message[:4096]

        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "HTML"
        }

        logger.debug("Sending Telegram message (bot token hidden).")
        response = requests.post(url, json=payload, timeout=10)

        # Prefer checking Telegram's 'ok' field as well as HTTP status
        try:
            data = response.json()
        except ValueError:
            logger.error("Telegram response is not JSON. Status: %s, Body: %s", response.status_code, response.text)
            return False

        if response.status_code == 200 and data.get("ok") is True:
            logger.info("Telegram message sent successfully.")
            return True

        logger.error("Failed to send Telegram message. Status: %s, ok: %s, body: %s", response.status_code, data.get("ok"), data)
        return False

    except Exception as e:
        logger.exception("Telegram error: %s", e)
        return False
