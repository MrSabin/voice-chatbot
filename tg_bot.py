import logging
import time
from functools import partial

import telegram
from environs import Env
from telegram import Update
from telegram.error import NetworkError
from telegram.ext import (CallbackContext, CommandHandler, Filters,
                          MessageHandler, Updater)

from detect_intent import detect_intent_texts
from logs_handler import BotLogsHandler

LANGUAGE_CODE = 'ru-RU'
logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext):
    update.message.reply_text("Здравствуйте!")


def reply(update: Update, context: CallbackContext, project_id):
    session_id = update.effective_user.id
    try:
        answer = detect_intent_texts(project_id, session_id, update.message.text, LANGUAGE_CODE)
        update.message.reply_text(answer.fulfillment_text)
    except NetworkError:
        logger.warning("Network error, retry")
        time.sleep(3)

def main():
    env = Env()
    env.read_env()
    tg_token = env.str("TG_BOT_TOKEN")
    project_id = env.str("PROJECT_ID")
    chat_id = env.str("TG_CHAT_ID")
    bot = telegram.Bot(token=tg_token)

    logger.setLevel(logging.INFO)
    handler = BotLogsHandler(bot, chat_id)
    formatter = logging.Formatter("%(process)d %(levelname)s %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.info("TG_bot started")

    updater = Updater(tg_token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text, partial(reply, project_id=project_id)))
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
