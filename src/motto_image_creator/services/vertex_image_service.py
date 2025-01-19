import os
from pathlib import Path
import vertexai
from vertexai.preview.vision_models import ImageGenerationModel
from ..constants import PROJECT_ID, LOCATION, MODEL_IMAGE_GENERATE, MODEL_IMAGE_NEGATIVE_PROMPT, MODEL_IMAGE_PERSON_GENERATION

def init_vertex():
    print(f"Initializing Vertex AI client with project ID: {PROJECT_ID} and location: {LOCATION}")
    vertexai.init(project=PROJECT_ID, location=LOCATION)

def generate_image(prompt: str, output_path: str | Path, image_extension: str) -> list[str]:
    """Generate an image using Vertex AI's Imagen model."""
    try:
        # Initialize the Imagen model
        model = ImageGenerationModel.from_pretrained(MODEL_IMAGE_GENERATE)
        
        # Generate the image
        print(f"Generating image with prompt: {prompt}")
        images = model.generate_images(
            prompt=prompt,
            negative_prompt=MODEL_IMAGE_NEGATIVE_PROMPT,
            number_of_images=4,
            language="en",
            aspect_ratio="1:1",
            safety_filter_level="block_some",
            person_generation=MODEL_IMAGE_PERSON_GENERATION,
            add_watermark=False
        )
        
        # Save the first generated image
        generated_images_filenames = []
        for i, image in enumerate(images):
            location=f"{output_path}_{i}.{image_extension}"
            generated_images_filenames.append(location)
            image.save(location, include_generation_parameters=False)
        return generated_images_filenames
    
    except Exception as e:

        raise Exception(f"Failed to generate image: {str(e)}")
