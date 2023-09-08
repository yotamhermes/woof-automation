import json
import requests
import os


def lambda_handler(event, context):

    CHAT_ID = os.getenv('CHAT_ID')
    BOT_TOKEN = os.getenv('BOT_TOKEN')

    message = event.get('message')

    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    params = {
        'chat_id': CHAT_ID,
        'text': message
    }

    response = requests.post(url, data=params)

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "response_text": response.text,
                "response_status_code": response.status_code
            }
        )
    }
