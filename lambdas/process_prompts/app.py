import os
import ai21
import json
import psycopg2
import requests
import boto3

DB_CONNECTION_STRING = os.getenv('DB_CONNECTION_STRING')
GENERATE_IMAGES_COUNT = 3



def lambda_handler(event, context):
    global conn
    conn = psycopg2.connect(DB_CONNECTION_STRING)

    ai21.api_key = os.getenv("AI21_API_KEY")

    status_code = 200
    message = "Done generating Post Suggestions"

    try:
        prompts = get_new_prompts_from_db()

        print(f"Got {len(prompts)} prompts from db")

        for prompt in prompts:
            prompt_id = prompt[0]
            prompt_text = prompt[1]

            print(f"start processing prompt with id {prompt_id}")

            images_urls = generate_images_from_prompt(prompt_id, prompt_text)

            post_suggestions = []

            for image_url in images_urls:
                caption = generate_caption_from_prompt(prompt_text)
                post_suggestions.append((prompt_id, caption, image_url))

            save_post_suggestions_to_db(prompt_id, post_suggestions)

            set_prompt_as_done(prompt_id)

            print(f"finished processing prompt with id {prompt_id}")

    except BaseException as e:
        print(e)
        status_code = 500
        message = "Error processing prompts"
    finally:
        conn.close()

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

        with conn.cursor() as cursor:
            cursor.execute(query)

            prompts = cursor.fetchall()

        return prompts
    except (Exception, psycopg2.Error) as error:
        print(f"Error fetching prompts: {error}")
        raise error


def generate_images_from_prompt(prompt_id, prompt_text):
    links = []

    for i in range(GENERATE_IMAGES_COUNT):
        binary_content = get_image_from_imagine(prompt_text)
        save_image_to_s3(binary_content, filename=f'{prompt_id}-{i + 1}.jpg')
        links.append(f'{prompt_id}-{i + 1}.jpg')

    return links


def get_image_from_imagine(prompt):
    url = os.getenv('IMAGINE_ENDPOINT')
    api_key = os.getenv('IMAGINE_API_KEY')

    headers = {
        'bearer': api_key
    }

    print(f"getting image from Imagine.Art to prompt {prompt}")

    # Using None here allows us to treat the parameters as string
    data = {
        'model_version': (None, '1'),
        'prompt': (None, prompt),
        'style_id': (None, '30'),
        'high_res_results': (None, '1'),
    }

    response = requests.post(url, headers=headers, files=data)

    if response.status_code == 200:
        return response.content
    else:
        print(
            f"Could Not Make request to Imagine.art, Response with code {response.status_code} and content {response.content}")
        raise BaseException(
            f"Could Not Make request to Imagine.art, Response with code {response.status_code}")


def save_image_to_s3(binary_content, filename):
    bucket = os.getenv('BUCKET_NAME')
    s3 = boto3.client('s3')
    
    with open(f'/tmp/{filename}', 'wb') as f:
        f.write(binary_content)

    s3.upload_file(f'/tmp/{filename}', bucket,
                   f'{filename}')


def generate_caption_from_prompt(prompt_text):
    message = f"""
    Generate caption for instagram post with post about '{prompt_text}',
    make it short and captivating
    """.replace("\n", "")

    print(f"getting caption from AI21 to prompt {prompt_text}")

    answer = ai21.Completion.execute(
        model="j2-ultra",
        prompt=message,
        maxTokens=300,
        temperature=1
    )

    answer = answer.completions[0].data.text

    caption = answer.replace("\"", "").replace("\'", "").replace("\n", "")

    return caption


# post suggestions is [(prompt_id, caption, image_url),...]
def save_post_suggestions_to_db(prompt_id, post_suggestions):
    try:
        with conn.cursor() as cursor:
            # cursor.mogrify() to insert multiple values
            args = ','.join(cursor.mogrify("(%s,%s,%s, 'NEW')", i).decode('utf-8')
                            for i in post_suggestions)

            insert_query = f"INSERT INTO post_suggestions (prompt_id, caption, image_link, status) VALUES {args}"

            cursor.execute(insert_query)

        conn.commit()

        print(f"generated post_suggestions for prompt {prompt_id} saved")

    except (Exception, psycopg2.Error) as error:
        print(f"Error saving post_suggestion: {error}")


def set_prompt_as_done(prompt_id):
    try:

        update_query = "UPDATE prompts SET status=(%s) WHERE prompt_id = (%s);"

        with conn.cursor() as cursor:
            cursor.execute(update_query, ('DONE', prompt_id))

        conn.commit()

        print(f"set prompt {prompt_id} as done")

    except (Exception, psycopg2.Error) as error:
        print(f"Error setting prompt as done: {error}")
