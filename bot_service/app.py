import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def handleMessage(update: Update, context: ContextTypes.DEFAULT_TYPE):
    post_idea = update.message.text

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Sounds Great, I will start working on creating images of `{post_idea}`"
    )

BOT_TOKEN = os.getenv('BOT_TOKEN')

if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    messageHandler = MessageHandler(
        filters.TEXT,
        handleMessage
    )

    application.add_handler(messageHandler)

    application.run_polling()
