from typing import Tuple
import google.generativeai as genai
from ..constants import MODEL_POEM, MODEL_IMAGE_PROMPT, MODEL_IMAGE_PROMPT_AVOID_PERSONS, MODEL_IMAGE_PROMPT_INCLUDE_POEM

def generate_poem(prompt: str) -> str:
    """Generate a poem using Gemini Pro model."""
    model = genai.GenerativeModel(MODEL_POEM)
    poem_prompt = prompt
    response = model.generate_content(poem_prompt)
    return response.text.strip()

def generate_image_prompt(topic: str | None, poem: str) -> str:
    """Generate an image prompt based on the topic and poem."""
    image_prompt = ""
    image_prompt += f"Create a very detailed image prompt for Google Imagen.\n\n"
    if topic:
        image_prompt += f"The topic is <topic>{topic}</topic>.\n"
    if MODEL_IMAGE_PROMPT_INCLUDE_POEM:
        image_prompt += f"The poem is:\n<poem>\n{poem}\n</poem>\n"
    image_prompt += "Besides the topic and the poem make the image specifically related to positive, constructive, user-centric, collaborative software-creating."
    image_prompt += "Focus on visual elements, style, and mood.\n"
    image_prompt += "The image should be a single image, not a collage.\n"
    image_prompt += "Make the image be a photo realistic image.\n"
    if MODEL_IMAGE_PROMPT_AVOID_PERSONS:
        print(" -> Avoiding persons as that might be restricted by the model which leads to no return of images in the end.")
        image_prompt += "It is very important that the image does not contain faces of persons, people, or people-like objects.\n"
        image_prompt += "You must still preserve the multiple person collaboration in the image e.g. by showing parts of people or persons or showing people in a group and from behind.\n"
        image_prompt += "Try to be creative in still giving the the image a good impression of multiple persons collaborating in a room, standing, ... in the mentioned setting.\n"
        image_prompt += "Avoid overusing of close-ups in general and also avoid showing only parts of people or persons.\n"
        image_prompt += "Still capture a full room, a full group of people, or a full group of persons.\n"
    
    image_prompt += "\nPlease return only the instructions. No intro or outro. Only the requested image generation instructions."
    
    generation_config = genai.GenerationConfig(temperature=0.8, max_output_tokens=1000)
    model = genai.GenerativeModel(MODEL_IMAGE_PROMPT, generation_config=generation_config)
    response = model.generate_content(image_prompt)
    return response.text.strip()
