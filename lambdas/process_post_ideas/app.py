import os
import ai21
import json
import psycopg2
import re


DB_CONNECTION_STRING = os.getenv('DB_CONNECTION_STRING')
conn = psycopg2.connect(DB_CONNECTION_STRING)
cursor = conn.cursor()


def lambda_handler(event, context):
    try:

        ideas = get_new_ideas_from_db()

        for idea in ideas:
            idea_id = idea[0],
            idea_text = idea[1]

            prompts = generate_prompts_from_idea(idea_text)
            save_prompts_to_db(prompts, idea_id)
            set_idea_as_done(idea_id)
    except:
        cursor.close()
        conn.close()
        return {
            "statusCode": 500,
            "body": json.dumps(
                {
                    "message": "Error generating prompts",
                }
            ),
        }

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": "Done generating prompts",
            }
        ),
    }


def get_new_ideas_from_db():
    try:
        query = "select post_idea_id, idea from post_ideas where status='NEW' and idea is not null"

        cursor.execute(query)

        post_ideas = cursor.fetchall()

        return post_ideas
    except (Exception, psycopg2.Error) as error:
        cursor.close()
        conn.close()
        print(f"Error fetching ideas: {error}")


def set_idea_as_done(idea_id):
    try:
        update_query = "UPDATE post_ideas SET status=(%s) WHERE post_idea_id = (%s);"

        cursor.execute(update_query, ('DONE', idea_id))

        # Commit the transaction and close the cursor and connection
        conn.commit()

    except (Exception, psycopg2.Error) as error:
        cursor.close()
        conn.close()
        print(f"Error saving idea: {error}")


def generate_prompts_from_idea(idea):
    ai21.api_key = os.getenv("AI21_API_KEY")

    message = f"""
    Generate a 5 item's numbered list of Image generation prompts for general idea {idea},
    humanize the dog as much as you can,
    Give details about the envirnment and the outfit,
    Every item on the list should be independent,
    Seperate image characteristics with comas
    """.replace("\n", "")

    answer = ai21.Completion.execute(
        model="j2-ultra",
        prompt=message,
        maxTokens=300,
        temperature=1
    )

    answer = answer.completions[0].data.text

    try:
        # regex of Number followed by dot and space: "1. "
        prompts = re.split(r'\d+\.\s', answer)

        # Remove any empty strings resulting from the split
        prompts = [prompt.strip() for prompt in prompts if prompt.strip()]

        return prompts

    except:
        cursor.close()
        conn.close()
        raise f"""Could not parse answer from ai labs:
            `{answer}`
        """


def save_prompts_to_db(prompts, idea_id):
    try:
        prompts_objects = [(prompt, idea_id, 'NEW') for prompt in prompts]

        # cursor.mogrify() to insert multiple values
        args = ','.join(cursor.mogrify("(%s,%s,%s)", i).decode('utf-8')
                        for i in prompts_objects)

        insert_query = f"INSERT INTO prompts (prompt, post_idea_id, status) VALUES {args}"

        cursor.execute(insert_query)

        # Commit the transaction and close the cursor and connection
        conn.commit()

        print(f"generated prompts for idea {idea_id} saved")

    except (Exception, psycopg2.Error) as error:
        cursor.close()
        conn.close()
        print(f"Error saving idea: {error}")
