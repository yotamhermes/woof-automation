import os
import openai
import json

openai.api_key = os.getenv("OPENAI_API_KEY")


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
    return ['Dog dressed as barby doll', 'Dog in paris']


def generate_prompts_from_ideas(ideas):
    message = f"""       
        Generate a 5 item's list of Image generation prompts for each of the following general ideas: 
        {ideas}
        Give details about the envirnment and the outfit. 
        Seperate characteristics with comas.
    """

    chat_completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": message}]
    )

def save_prompts_to_db(prompts):
    return "saved"