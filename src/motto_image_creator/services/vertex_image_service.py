import os
from pathlib import Path
import vertexai
from vertexai.preview.vision_models import ImageGenerationModel
from ..constants import PROJECT_ID, LOCATION, MODEL_NAME

def init_vertex():
    vertexai.init(project=PROJECT_ID, location=LOCATION)

def generate_image(prompt: str, output_path: str | Path) -> str:
    """Generate an image using Vertex AI's Imagen model."""
    try:
        init_vertex()
        
        # Initialize the Imagen model
        model = ImageGenerationModel.from_pretrained(MODEL_NAME)
        
        # Generate the image
        images = model.generate_images(
            prompt=prompt,
            number_of_images=1,
            language="en",
            aspect_ratio="1:1",
            safety_filter_level="block_some",
        )
        
        # Create output directory if it doesn't exist
        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        
        # Save the first generated image
        images[0].save(location=output_path, include_generation_parameters=False)
        return str(output_path)
    
    except Exception as e:
        raise Exception(f"Failed to generate image: {str(e)}")
