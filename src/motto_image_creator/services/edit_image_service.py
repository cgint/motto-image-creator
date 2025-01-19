from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import os
from ..constants import TEXT_FONT_PATH

def create_rounded_rectangle(width: int, height: int, radius: int, color: tuple) -> Image.Image:
    """Create a rounded rectangle image."""
    rectangle = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(rectangle)
    draw.rounded_rectangle([(0, 0), (width, height)], radius=radius, fill=color)
    return rectangle


def get_font(font_size: int) -> ImageFont.ImageFont:
    return ImageFont.truetype(TEXT_FONT_PATH, size=font_size)


def draw_box_with_text(img, text_lines, text_box_x, text_box_y, text_box_width, text_box_height, text_box_color, text_padding, radius, font, font_size, font_color):
    y_text = text_box_y + text_padding
    line_spacing = text_padding
    text_box_height = len(text_lines) * (font_size + line_spacing) + 2*text_padding if text_box_height is None else text_box_height
    text_box = create_rounded_rectangle(text_box_width, text_box_height, radius, text_box_color)
    img.paste(text_box, (text_box_x, text_box_y), text_box)

    # Add text
    draw = ImageDraw.Draw(img)
    for line in text_lines:
        line_width = draw.textlength(line, font=font)
        x_text = text_box_x + (text_box_width - line_width) // 2
        draw.text((x_text, y_text), line, font=font, fill=font_color)
        y_text += font_size + line_spacing

def add_text_box_poem(img, text, text_box_width, text_box_radius, font_size, font_color, text_box_color):
    # Create semi-transparent box for text
    text_box_height = None # auto-calculate
    text_box_x = (img.width - text_box_width) // 2
    text_box_y = 40 # (img.height - text_box_height) // 2
    text_padding = 20

    # Use default font if custom font not available
    text_lines = text.strip().split("\n")
    longest_line_len = max(len(line) for line in text_lines)
    font_size_line_len_corrected = font_size 
    if longest_line_len > 30:
        font_size_line_len_corrected = font_size - (longest_line_len - 30)
        print(f"Font size corrected for line length: {font_size_line_len_corrected}")
    font = get_font(font_size_line_len_corrected)

    draw_box_with_text(img, text_lines, text_box_x, text_box_y, text_box_width, text_box_height, text_box_color, text_padding, text_box_radius, font, font_size, font_color)

def add_text_box_credits(img, text, text_box_width, text_box_radius, font_size, font_color, text_box_color):
    # Create semi-transparent box for text
    text_box_height = 40
    text_box_x = (img.width - text_box_width) // 2
    text_box_y = (img.height - text_box_height) - 20
    text_padding = 10
    # Use default font if custom font not available
    font = get_font(font_size)
    text_lines = text.strip() .split("\n")

    draw_box_with_text(img, text_lines, text_box_x, text_box_y, text_box_width, text_box_height, text_box_color, text_padding, text_box_radius, font, font_size, font_color)

def add_text_to_image(
    image_path: str | Path,
    text_poem: str,
    text_credits: str,
    output_path: str | Path
):
    """Add text to an image with a semi-transparent background box."""
    # Create a blank image if input doesn't exist yet
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Input image file not found: {image_path}")
    print(f"Adding text to image: {image_path} -> {output_path}")
    img = Image.open(image_path)
    img = img.convert('RGBA')
        
    # Resize image to 1024x1024
    img = img.resize((1024, 1024))

    # Add rounded borders (50px)
    text_box_radius = 50
    text_box_width = 960
    font_size_poem = 42
    font_size_credits = 18
    font_color = (137, 242, 188)
    text_box_color = (0, 0, 0, 200)  # Semi-transparent black

    add_text_box_poem(img, text_poem, text_box_width, text_box_radius, font_size_poem, font_color, text_box_color)
    add_text_box_credits(img, text_credits, text_box_width, text_box_radius, font_size_credits, font_color, text_box_color)

    # Save image
    img.save(output_path)
