import json
import psycopg2
import os

DB_CONNECTION_STRING = os.getenv('DB_CONNECTION_STRING')


def lambda_handler(event, context):
    print(f'Got event: {event}')

    prompt_id = json.loads(event.get('body')).get('prompt_id')

    global conn
    global cursor

    conn = psycopg2.connect(DB_CONNECTION_STRING)
    cursor = conn.cursor()

    if prompt_id is None:
        return {
            "statusCode": 400,
            "body": json.dumps(
                {
                    "message": "Got Empty PromptId",
                }
            ),
        }

    status_code = 200
    message = f"All posts create by prompt {prompt_id} marked as done"

    try:
        mark_post_suggestions_as_done(prompt_id)
    except:
        cursor.close()
        conn.close()
        status_code = 500
        message = "Error generating prompts"

    return {
        "statusCode": status_code,
        "body": json.dumps(
            {
                "message": message
            }
        ),
    }


def mark_post_suggestions_as_done(prompt_id):
    try:
        update_query = "UPDATE post_suggestions SET status=(%s) WHERE prompt_id = (%s);"

        with conn.cursor() as cursor:
            cursor.execute(update_query, ('DONE', prompt_id))

        conn.commit()

        print(f"set post suggestions created by {prompt_id} as done")

    except (Exception, psycopg2.Error) as error:
        print(f"Error setting post suggestions as done: {error}")
