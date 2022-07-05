import logging
from telegram import Update, Chat, constants, error
from telegram.ext import ApplicationBuilder, CallbackContext, CommandHandler, MessageHandler, filters, ChatMemberHandler
import config.SECRETS

TOKEN = config.SECRETS.TOKEN

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
        except error.Forbidden:
            pass


def main():
    application = ApplicationBuilder().token(config.SECRETS.TOKEN).build()

    handlers = {0: [CommandHandler('start', start),
                    ChatMemberHandler(generic_message)
                    ]}
    application.add_handlers(handlers)
    application.run_polling()


if __name__ == '__main__':
    main()
