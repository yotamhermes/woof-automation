import json


def lambda_handler(event, context):
    """
        Parameters
        ----------
        event : dict
            a dict contains { topic, number_of_prompts: 5}
    """

    topic = event.get('topic')
    number_of_prompts = event.get('number_of_prompts')

    if topic is None:
        return "topic was not passed to function"
    
    if number_of_prompts is None:
        number_of_prompts = 5

    images = generate_images_from_topic(topic)

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": "hello world this is yotam",
            }
        ),
    }

def generate_images_from_topic(topic, number_of_prompts):
    prompts = get_prompts(topic, number_of_prompts)
    images = []

    for prompt in prompts:
        image = get_image(prompt)
        images.append(image)

    return images

def get_prompts(topic, number_of_prompts):
    return ["prompt 1", "prompt 2", "prompt 3", "prompt 4", "prompt 5"]

def get_image(prompt):
    return "this_is_an_image"