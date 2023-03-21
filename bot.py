from environs import Env
from telegram import ForceReply, Update
from telegram.ext import (CallbackContext, CommandHandler, Filters,
                          MessageHandler, Updater)


def start(update: Update, context: CallbackContext):
    user = update.effective_user
    update.message.reply_text("Здравствуйте!")


def echo(update, context):
    update.message.reply_text(update.message.text)


def main():
    env = Env()
    env.read_env()
    tg_token = env.str("TG_BOT_TOKEN")
    updater = Updater(tg_token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text, echo))
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
