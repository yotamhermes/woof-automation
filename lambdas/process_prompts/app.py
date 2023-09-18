import os
import ai21
import json
import psycopg2
import re


DB_CONNECTION_STRING = os.getenv('DB_CONNECTION_STRING')
GENERATE_IMAGES_COUNT = 2

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
            
            for image_url in images_urls:
                save_post_suggestions(prompt_id, image_url, caption)
                
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
    return []

def generate_image_from_prompt(prompt_text):
    return ['s3:\\image_1', "s3:\\image2"]

def generate_caption_from_prompt(prompt_text):
    return "This is a short caption"

def save_post_suggestions(prompt_id, image_url, caption):
    return -1 # newly prompt created id

def set_prompt_as_done(prompt_id):
    print("done")