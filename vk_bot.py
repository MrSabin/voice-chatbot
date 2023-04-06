import logging
import time
from random import randint

import telegram
import vk_api as vk
from environs import Env
from requests.exceptions import ConnectionError
from vk_api.longpoll import VkEventType, VkLongPoll

from detect_intent import detect_intent_texts

LANGUAGE_CODE = 'ru-RU'
logger = logging.getLogger(__name__)


class BotLogsHandler(logging.Handler):
    def __init__(self, bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.bot = bot

    def emit(self, record):
        log_entry = self.format(record)
        self.bot.send_message(chat_id=self.chat_id, text=log_entry)


def reply(event, vk_api, project_id):
    session_id = event.user_id
    answer = detect_intent_texts(
        project_id, session_id, event.text, LANGUAGE_CODE)
    if not answer.intent.is_fallback:
        vk_api.messages.send(
            user_id=event.user_id,
            message=answer.fulfillment_text,
            random_id=randint(1, 100000)
        )


if __name__ == "__main__":
    env = Env()
    env.read_env()
    vk_token = env.str("VK_TOKEN")
    tg_token = env.str("TG_BOT_TOKEN")
    chat_id = env.str("TG_CHAT_ID")
    project_id = env.str("PROJECT_ID")
    bot = telegram.Bot(token=tg_token)

    logger.setLevel(logging.INFO)
    handler = BotLogsHandler(bot, chat_id)
    formatter = logging.Formatter("%(process)d %(levelname)s %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.info("VK_bot started")

    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        try:
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                reply(event, vk_api, project_id)
        except ConnectionError:
            logger.warning("Connection lost, retry")
            time.sleep(3)