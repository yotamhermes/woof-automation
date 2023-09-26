import os
import json
import psycopg2


DB_CONNECTION_STRING = os.getenv('DB_CONNECTION_STRING')
URL_PREFIX = os.getenv('URL_PREFIX')


def lambda_handler(event, context):
    status_code = 200
    posts_suggestions = []

    global conn
    global cursor

    conn = psycopg2.connect(DB_CONNECTION_STRING)
    cursor = conn.cursor()

    try:
        posts_suggestions = get_new_posts_suggestions()
        posts_suggestions = process_suggestions(posts_suggestions)
    except:
        cursor.close()
        conn.close()
        status_code = 500

    return {
        "statusCode": status_code,
        "body": json.dumps(posts_suggestions),
        'headers': {
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,GET'
        },
    }


def process_suggestions(posts_suggestions):
    parsed = {}

    for post_suggestion in posts_suggestions:
        prompt_id, caption, image = post_suggestion

        if prompt_id not in parsed:
            parsed[prompt_id] = {
                'created_from_prompt': prompt_id,
                'images': [],
                'captions': []
            }

        parsed[prompt_id]['images'].append(f'{URL_PREFIX}/{image}')
        parsed[prompt_id]['captions'].append(caption)

    return list(parsed.values())


def get_new_posts_suggestions():
    try:
        print(f"getting new post suggestions from db")

        query = "SELECT prompt_id, caption, image_link FROM public.post_suggestions where status = 'NEW'"

        cursor.execute(query)

        posts_suggestions = cursor.fetchall()

        return posts_suggestions
    except (Exception, psycopg2.Error) as error:
        cursor.close()
        conn.close()
        print(f"Error fetching ideas: {error}")
