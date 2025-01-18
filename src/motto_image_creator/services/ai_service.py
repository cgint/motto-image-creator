import os
from typing import Tuple
import google.generativeai as genai
from ..constants import api_key, MODEL_POEM, MODEL_IMAGE_PROMPT, MODEL_IMAGE_GENERATE

def init_genai():
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is not set")
    genai.configure(api_key=api_key)

def generate_poem(prompt: str) -> str:
    """Generate a poem using Gemini Pro model."""
    model = genai.GenerativeModel(MODEL_POEM)
    poem_prompt = f"Create a poem about {prompt}. Make it concise and impactful."
    response = model.generate_content(poem_prompt)
    return response.text

def generate_image_prompt(topic: str) -> str:
    """Generate an image prompt based on the topic."""
    model = genai.GenerativeModel(MODEL_IMAGE_PROMPT)
    image_prompt = f"Create a detailed image prompt for: {topic}. Focus on visual elements, style, and mood."
    response = model.generate_content(image_prompt)
    return response.text

def generate_content(prompt: str) -> Tuple[str, str]:
    """Generate both poem and image prompt."""
    poem = generate_poem(prompt)
    image_prompt = generate_image_prompt(prompt)
    return poem, image_prompt
