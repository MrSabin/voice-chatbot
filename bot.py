from functools import partial

from environs import Env
from telegram import Update
from telegram.ext import (CallbackContext, CommandHandler, Filters,
                          MessageHandler, Updater)

from detect_intent import detect_intent_texts

LANGUAGE_CODE = 'ru-RU'


def start(update: Update, context: CallbackContext):
    update.message.reply_text("Здравствуйте!")


def reply(update: Update, context: CallbackContext, project_id):
    session_id = update.effective_user.id
    answer = detect_intent_texts(project_id, session_id, update.message.text, LANGUAGE_CODE)
    update.message.reply_text(answer.fulfillment_text)

def main():
    env = Env()
    env.read_env()
    tg_token = env.str("TG_BOT_TOKEN")
    project_id = env.str("PROJECT_ID")
    updater = Updater(tg_token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text, partial(reply, project_id=project_id)))
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
