from PIL import Image, ImageDraw, ImageFont
import textwrap
from pathlib import Path
import os
import google.generativeai as genai

def init_genai():
    """Initialize the Gemini client."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is not set")
    genai.configure(api_key=api_key)

def generate_image(prompt: str, output_path: str | Path) -> str:
    """Generate an image using Gemini's Imagen model."""
    try:
        init_genai()
        model = genai.GenerativeModel('imagen-3.0-generate-002')
        response = model.generate_image(
            prompt=prompt,
            negative_prompt="people",
            number_of_images=1,
            aspect_ratio="1:1"
        )
        
        # Save the generated image
        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
            
        # Save the first generated image
        response.image.save(output_path)
        return str(output_path)
    except Exception as e:
        raise Exception(f"Failed to generate image: {str(e)}")

def create_rounded_rectangle(width: int, height: int, radius: int, color: tuple) -> Image.Image:
    """Create a rounded rectangle image."""
    rectangle = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(rectangle)
    draw.rounded_rectangle([(0, 0), (width, height)], radius=radius, fill=color)
    return rectangle

def add_text_to_image(
    image_path: str | Path,
    text: str,
    output_path: str | Path = "output.png"
) -> str:
    """Add text to an image with a semi-transparent background box."""
    # Ensure the output directory exists
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    # Create a blank image if input doesn't exist yet
    if not os.path.exists(image_path):
        img = Image.new('RGB', (1024, 1024), (0, 0, 0))
    else:
        img = Image.open(image_path)
        img = img.convert('RGBA')
        
    # Resize image to 1024x1024
    img = img.resize((1024, 1024))
    draw = ImageDraw.Draw(img)

    # Add rounded borders (50px)
    width, height = img.size
    radius = 50
    rounded_rect = create_rounded_rectangle(width, height, radius, (0, 0, 0, 0))
    img.paste(rounded_rect, (0, 0), rounded_rect)

    # Create semi-transparent box for text
    text_box_width = 800
    text_box_height = 500
    text_box_x = (width - text_box_width) // 2
    text_box_y = (height - text_box_height) // 2
    text_box_color = (0, 0, 0, 128)  # Semi-transparent black

    text_box = create_rounded_rectangle(text_box_width, text_box_height, 20, text_box_color)
    img.paste(text_box, (text_box_x, text_box_y), text_box)

    # Use default font if custom font not available
    font = ImageFont.load_default()
    font_size = 30

    # Wrap text
    wrapped_text = textwrap.wrap(text, width=40)

    # Add text
    y_text = text_box_y + 20
    line_spacing = 10

    for line in wrapped_text:
        line_width = draw.textlength(line, font=font)
        x_text = text_box_x + (text_box_width - line_width) // 2
        draw.text((x_text, y_text), line, font=font, fill=(255, 255, 255))
        y_text += font_size + line_spacing

    # Save image
    img.save(output_path)
    return str(output_path)
