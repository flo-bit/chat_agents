import os
import requests
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY')
)


async def create_images(texts: str, paths: str, model="dall-e-3"):
    for text, path in zip(texts, paths):
        await create_image(text, path, model)


async def create_image(text: str, path: str, model="dall-e-3"):
    response = client.images.generate(
        model=model,
        prompt=text,
        size="1024x1024",
        quality="standard",
        n=1,
    )

    image_url = response.data[0].url

    # download image
    image = requests.get(image_url).content

    # save image
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(image)

    return "image saved to " + path

tool_create_image = ({
    "type": "function",
    "function": {
            "name": "create_image",
            "description": "Creates a png image from given image prompt.",
            "parameters": {
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": "prompt to convert to image, should be very descriptive at least 50 words long, max 200 words",
                    },
                    "path": {
                        "type": "string",
                        "description": "Path to save image to, relative to the current working directory"
                    },
                    "model": {
                        "type": "string",
                        "description": "model to use for image generation, defaults to dall-e-3",
                        "enum": ["dall-e-2", "dall-e-3"]
                    },
                    "size": {
                        "type": "string",
                        "description": "size of image to generate, defaults to 1024x1024",
                        "enum": ["256x256", "512x512", "1024x1024"]
                    }
                },
                "required": ["prompt", "path"],
            },
    }
}, create_image)

tool_create_images = ({
    "type": "function",
    "function": {
            "name": "create_images",
            "description": "Creates png images from given image prompts.",
            "parameters": {
                "type": "object",
                "properties": {
                    "prompts": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "description": "prompt to convert to image, should be very descriptive at least 50 words long, max 200 words",
                        },
                        "description": "Image prompts"
                    },
                    "paths": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "description": "Path to save image to, relative to the current working directory"
                        },
                        "description": "Paths to save images to"
                    },
                    "model": {
                        "type": "string",
                        "description": "model to use for image generation, defaults to dall-e-3",
                        "enum": ["dall-e-2", "dall-e-3"]
                    },
                },
                "required": ["prompts", "paths"],
            },
    }
}, create_images)
