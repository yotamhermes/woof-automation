import logging
import os
from telegram import Update, MenuButtonWebApp, WebAppInfo, Bot
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import requests

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def handleMessage(update: Update, context: ContextTypes.DEFAULT_TYPE):
    post_idea = update.message.text

    # save_to_db(post_idea)

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
APP_URL = os.getenv('APP_URL')

if __name__ == '__main__':
    web_app = WebAppInfo(url=APP_URL)

    menu_button = MenuButtonWebApp(text='Review Posts', web_app=web_app)

    bot = Bot(token=BOT_TOKEN)

    bot.set_chat_menu_button(menu_button=menu_button)

    application = ApplicationBuilder().bot(bot).build()

    messageHandler = MessageHandler(
        filters.TEXT,
        handleMessage
    )

    application.add_handler(messageHandler)

    application.run_polling()
