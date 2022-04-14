# For testing
# import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
# import configparser
import logging
import configparser

HELP_MSG = "Available commands:\n" \
               "    /help -- List all the commends\n" \
               "    /workoutPlan -- Check your own gym plan\n" \
               "    /groups -- Gym by selecting major muscle groups in your body\n" \
               "    /tips -- Getting some random gym tips everyday!\n" \

DESP = "This is a gym manegment chatbot that delivers fitness workouts that don't require a gym.Each workout is optimized to be efficient and effective!\n"\
               "    See what I can do by sending '/help'\n" \


def main():
    # Load your token and create an Updater for your Bot
    config = configparser.ConfigParser()
    config.read('config.ini')
    updater = Updater(
        token=(config['TELEGRAM']['ACCESS_TOKEN']), use_context=True)
    dispatcher = updater.dispatcher

    # You can set this logging module, so you will know when and why things do not work as expected
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    # register a dispatcher to handle message: here we register an echo dispatcher
    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    dispatcher.add_handler(echo_handler)

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("hello", hello))
    dispatcher.add_handler(CommandHandler("start", start))

    # To start the bot:
    updater.start_polling()
    updater.idle()


def echo(update, context):
    reply_message = update.message.text.upper()
    logging.info("Update: " + str(update))
    logging.info("context: " + str(context))
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=reply_message)

def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    logging.info("/help call")
    update.message.reply_text(DESP)

def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    logging.info("/help call")
    update.message.reply_text(HELP_MSG)


def hello(update, context) -> None:
    """Send a exactly reply when the command /hello <context> is issued."""
    try:
        user_says = " ".join(context.args)
        update.message.reply_text("Good day," + user_says + "!")
    except (IndexError, ValueError):
        update.message.reply_text('Usage: /hello <keyword>')


if __name__ == '__main__':
    main()
