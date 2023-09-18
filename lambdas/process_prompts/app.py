import os
import ai21
import json
import psycopg2
import re


DB_CONNECTION_STRING = os.getenv('DB_CONNECTION_STRING')
GENERATE_IMAGES_COUNT = 2

conn = psycopg2.connect(DB_CONNECTION_STRING)
cursor = conn.cursor()

def lambda_handler(event, context):
    status_code = 200
    message = "Done generating Post Suggestions"

    try:
        prompts = get_new_prompts_from_db()
        
        print(f"Got {len(prompts)} ideas from db")

        for prompt in prompts:
            prompt_id = prompt[0],
            prompt_text = prompt[1]

            print(f"start processing prompt with id {prompt_id}")

            images_urls = generate_image_from_prompt(prompt_text)
            caption = generate_caption_from_prompt(prompt_text)
            
            post_suggestions = []

            for image_url in images_urls:
                post_suggestions.append((prompt_id, caption, image_url))
            
            save_post_suggestions_to_db(prompt_id, post_suggestions)

            set_prompt_as_done(prompt_id)

            print(f"finished processing prompt with id {prompt_id}")

    except:
        status_code = 500
        message = "Error processing prompts"

    return {
        "statusCode": status_code,
        "body": json.dumps(
            {
                "message": message,
            }
        ),
    }

def get_new_prompts_from_db():
    try:
        print(f"getting prompts from db")

        query = "select prompt_id, prompt from prompts where status='NEW'"

        cursor.execute(query)

        prompts = cursor.fetchall()

        return prompts
    except (Exception, psycopg2.Error) as error:
        cursor.close()
        conn.close()
        print(f"Error fetching prompts: {error}")
        raise error

def generate_image_from_prompt(prompt_text):
    return ['s3:\\image_1', "s3:\\image2"]

def generate_caption_from_prompt(prompt_text):
    return "This is a short caption"

# post suggestions is [(prompt_id, caption, image_url),...]
def save_post_suggestions_to_db(prompt_id, post_suggestions):
    try:
        # cursor.mogrify() to insert multiple values
        args = ','.join(cursor.mogrify("(%s,%s,%s)", i).decode('utf-8')
                        for i in post_suggestions)

        insert_query = f"INSERT INTO prompts (prompt_id, caption, image_link) VALUES {args}"

        cursor.execute(insert_query)

        # Commit the transaction and close the cursor and connection
        conn.commit()

        print(f"generated post_suggestions for prompt {prompt_id} saved")

    except (Exception, psycopg2.Error) as error:
        cursor.close()
        conn.close()
        print(f"Error saving idea: {error}")

def set_prompt_as_done(prompt_id):
    try:

        update_query = "UPDATE prompts SET status=(%s) WHERE prompt_id = (%s);"

        cursor.execute(update_query, ('DONE', prompt_id))

        # Commit the transaction and close the cursor and connection
        conn.commit()

        print(f"set prompt {prompt_id} as done")

    except (Exception, psycopg2.Error) as error:
        cursor.close()
        conn.close()
        print(f"Error setting prompt as done: {error}")