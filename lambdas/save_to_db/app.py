import json
import psycopg2
import os

DB_CONNECTION_STRING = os.getenv('DB_CONNECTION_STRING')


def lambda_handler(event, context):
    idea = json.loads(event.get('body')).get('idea')

    print(f'Got event: {event}')

    if idea is None:
        return {
            "statusCode": 400,
            "body": json.dumps(
                {
                    "message": "Got Empty Idea",
                }
            ),
        }

    idea_id = save_post_idea(idea)

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": f"post_idea saved to db with id: {idea_id}",
            }
        ),
    }


def save_post_idea(idea_text):
    try:
        conn = psycopg2.connect(DB_CONNECTION_STRING)

        cursor = conn.cursor()

        insert_query = "INSERT INTO post_ideas (idea, status) VALUES (%s, %s) RETURNING post_idea_id;"

        cursor.execute(insert_query, (idea_text, 'NEW'))
        idea_id = cursor.fetchone()[0]

        # Commit the transaction and close the cursor and connection
        conn.commit()
        cursor.close()
        conn.close()

        print(f"Idea saved: {idea_text}")

        return idea_id
    except (Exception, psycopg2.Error) as error:
        print(f"Error saving idea: {error}")
