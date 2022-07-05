import logging

import telegram
from telegram import Update, Chat, constants, error
from telegram.ext import ApplicationBuilder, CallbackContext, CommandHandler, MessageHandler, filters, ChatMemberHandler
import config.SECRETS

TOKEN = config.SECRETS.TOKEN
OWNER_ID = config.SECRETS.OWNER_ID

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.WARNING,
)


async def start(update: Update, context: CallbackContext):
    if update.effective_chat.type == Chat.PRIVATE:
        await update.effective_chat.send_message(text=f"Your user ID: <code>{update.effective_user.id}</code>",
                                                 parse_mode=constants.ParseMode.HTML)


async def generic_message(update: Update, context: CallbackContext):
    if update.effective_chat.type == Chat.CHANNEL:
        try:
            await update.effective_chat.send_message(text=f"Channel chat ID: <code>{update.effective_chat.id}</code>",
                                                     parse_mode=constants.ParseMode.HTML)
            await update.effective_chat.leave()
        # Yes this is indeed the laziest way possible I could prevent the bot throwing an error when leaving a channel!
        except error.Forbidden:
            pass


async def kill(update: Update, context: CallbackContext):
    if update.effective_user.id == OWNER_ID and update.effective_chat.type == telegram.Chat.PRIVATE:
        await update.effective_chat.send_message(text=f"Killing bot")
        exit()


def main():
    application = ApplicationBuilder().token(config.SECRETS.TOKEN).build()

    handlers = {0: [CommandHandler('start', start),
                    CommandHandler('kill', kill),
                    ChatMemberHandler(generic_message)
                    ]}
    application.add_handlers(handlers)
    application.run_polling()


if __name__ == '__main__':
    main()
