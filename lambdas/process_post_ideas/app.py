import os
import openai
import json
import psycopg2


def lambda_handler(event, context):
    ideas = get_new_ideas_from_db()

    prompts = generate_prompts_from_ideas(ideas)

    save_prompts_to_db(prompts)

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": "hello world this is yotam version 2",
            }
        ),
    }


def get_new_ideas_from_db():
    DB_CONNECTION_STRING = os.getenv('DB_CONNECTION_STRING')

    try:
        conn = psycopg2.connect(DB_CONNECTION_STRING)

        cursor = conn.cursor()
        query = "select idea from post_ideas where status='NEW' and idea is not null"

        cursor.execute(query)

        post_ideas = cursor.fetchall()
        post_ideas = [i[0] for i in post_ideas]

        return post_ideas
    except (Exception, psycopg2.Error) as error:
        print(f"Error fetching ideas: {error}")


def generate_prompts_from_ideas(ideas):
    # openai.api_key = os.getenv("OPENAI_API_KEY")

    message = f"""       
        Generate a 5 item's list of Image generation prompts for each of the following general ideas: 
        {ideas}
        Give details about the envirnment and the outfit. 
        Seperate characteristics with comas.
    """

    # chat_completion = openai.ChatCompletion.create(
    #     model="gpt-3.5-turbo",
    #     messages=[{"role": "user", "content": message}]
    # )


def save_prompts_to_db(prompts):
    return "saved"
