import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import requests

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def handleMessage(update: Update, context: ContextTypes.DEFAULT_TYPE):
    post_idea = update.message.text

    save_to_db(post_idea)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Sounds great!\nI will start working on generating posts about `{post_idea}`"
    )


def save_to_db(idea):
    WOOF_ENDPOINT = os.getenv('WOOF_ENDPOINT')
    API_KEY = os.getenv('WOOF_API_KEY')

    # The API endpoint
    url = F"{WOOF_ENDPOINT}/save-to-db"

    headers = {"x-api-key": API_KEY}
    data = {"idea": idea}

    post_response = requests.post(url, json=data, headers=headers)
    logging.info(post_response)


BOT_TOKEN = os.getenv('BOT_TOKEN')

if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    messageHandler = MessageHandler(
        filters.TEXT,
        handleMessage
    )

    application.add_handler(messageHandler)

    application.run_polling()
