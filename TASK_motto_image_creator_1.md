
This is the result of me composing image and text in GIMP. The background image was done by Google Gemini Imagen 3 and the Poem-Text was done by LLM based on a prompt of me saying "Create a poem about creating user-centric software applications"

What i would like to have is a python program that does that automatically for me.The steps I did manually were:

*   Ask an LLM for a poem based on the prompt above
    
*   Ask Imagen 3 for an image reflecting the prompt
    
*   Do a lot of tedious composing in GIMP to have the image be 1024x24 with 50px rounded borders and then have an area with semi-transparent background that serves as a box for the poem
    

Please help me create such an automation in python using Google Gemini APIfor the AI-Parts

Okay, I understand. You want to automate the process of creating an image with text, similar to what you did manually in GIMP. This involves generating a poem with an LLM, creating a suitable image with an image generation model, and then compositing them together.

Here's a Python program that will help you do this using the Google Gemini API for both text and image generation, and the Pillow (PIL) library for image manipulation:

```python
import google.generativeai as genai
from PIL import Image, ImageDraw, ImageFont
import textwrap
import requests
import os

# Set your API key as an environment variable
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def generate_poem(prompt):
    """Generates a poem using the Gemini Pro model."""
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    return response.text

def generate_image(prompt, image_path="generated_image.png"):
    """Generates an image using the Gemini Pro Vision model and saves it."""
    model = genai.GenerativeModel('gemini-pro-vision')

    # Create a dummy image for the initial prompt (Imagen 3 doesn't have an API yet)
    dummy_image = Image.new("RGB", (1024, 1024), color="white")
    dummy_image.save("dummy.png")
    dummy_image = Image.open("dummy.png")

    response = model.generate_content(
        [prompt, dummy_image],
        safety_settings=[
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_NONE",
            },
        ]
    )

    # Extract the image URL from the response (simulating Imagen 3)
    # Assuming the response contains an image URL
    # Replace this with the actual logic to get the image URL from Gemini's response
    image_url = response.text  # This is a placeholder. Adjust as needed.

    # Download the image
    response = requests.get(image_url, stream=True)
    response.raise_for_status()  # Ensure the download was successful

    with open(image_path, 'wb') as file:
        for chunk in response.iter_content(8192):
            file.write(chunk)

    return image_path

def create_rounded_rectangle(width, height, radius, color):
    """Creates a rounded rectangle image."""
    rectangle = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(rectangle)

    # Draw the rounded rectangle
    draw.rounded_rectangle([(0, 0), (width, height)], radius=radius, fill=color)

    return rectangle

def add_text_to_image(image_path, text, output_path="output.png"):
    """Adds text to an image with a semi-transparent background box."""
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)

    # Resize image to 1024x1024
    img = img.resize((1024, 1024))

    # Add rounded borders (50px)
    width, height = img.size
    radius = 50
    rounded_rect = create_rounded_rectangle(width, height, radius, (0, 0, 0, 0))
    img.paste(rounded_rect, (0, 0), rounded_rect)

    # Create a semi-transparent box for the text
    text_box_width = 800
    text_box_height = 500  # Adjust height as needed
    text_box_x = (width - text_box_width) // 2
    text_box_y = (height - text_box_height) // 2
    text_box_color = (0, 0, 0, 128)  # Semi-transparent black

    text_box = create_rounded_rectangle(text_box_width, text_box_height, 20, text_box_color)
    img.paste(text_box, (text_box_x, text_box_y), text_box)

    # Choose a font and size
    try:
        font = ImageFont.truetype("arial.ttf", 30)  # You may need to change the font path
    except IOError:
        font = ImageFont.load_default()

    # Wrap the text to fit the box
    wrapped_text = textwrap.wrap(text, width=40)  # Adjust width as needed

    # Calculate text position within the box
    y_text = text_box_y + 20  # Start padding from the top of the box
    line_spacing = 10

    # Add the text to the image
    for line in wrapped_text:
        line_width, line_height = draw.textsize(line, font=font)
        x_text = text_box_x + (text_box_width - line_width) // 2
        draw.text((x_text, y_text), line, font=font, fill=(255, 255, 255))  # White text
        y_text += line_height + line_spacing

    # Save the image
    img.save(output_path)

# Main execution
if __name__ == "__main__":
    user_prompt = "Create a poem about creating user-centric software applications"

    # 1. Generate Poem
    poem = generate_poem(user_prompt)
    print("Generated Poem:\n", poem)

    # 2. Generate Image (Placeholder - Adapt when Gemini Image API is available)
    image_prompt = "A person coding on a computer in a modern, well-lit workspace"  # Example prompt
    generated_image_path = generate_image(image_prompt)
    print("Image generated at:", generated_image_path)

    # 3. Combine Image and Text
    add_text_to_image(generated_image_path, poem)
    print("Final image saved to output.png")
```

content\_copydownloadUse code [with caution](https://support.google.com/legal/answer/13505487).Python

**Explanation and Important Notes:**

1.  **API Key:**
    
    *   Make sure you have a Google Cloud Project set up and have enabled the Generative Language API.
        
    *   Obtain an API key and set the GOOGLE\_API\_KEY environment variable.
        
2.  **Dependencies:**
    
    *   pip install google-generativeai pillow requestscontent\_copydownloadUse code [with caution](https://support.google.com/legal/answer/13505487).Bash
        
3.  **Gemini Pro and Pro Vision:**
    
    *   The code uses gemini-pro for text generation (poem).
        
    *   The gemini-pro-vision is used, but it's a placeholder. The actual Gemini image generation API is not yet publicly available.
        
    *   You will likely need to adapt the generate\_image function when a proper image generation API becomes available.
        
4.  **Image Generation Placeholder:**
    
    *   The generate\_image function currently simulates the process of getting an image URL. It downloads the image and saves it. Replace the placeholder image\_url with the actual URL from the Gemini API when it becomes available.
        
    *   A dummy image is used to work around the issue that the Gemini API is not yet publicly available.
        
5.  **Image Manipulation (Pillow):**
    
    *   create\_rounded\_rectangle: Creates a rounded rectangle for borders and the text background.
        
    *   add\_text\_to\_image:
        
        *   Resizes the image to 1024x1024.
            
        *   Adds rounded borders using the rounded\_rect.
            
        *   Creates a semi-transparent text box.
            
        *   Loads a font (you might need to adjust the font path).
            
        *   Wraps the text to fit within the box.
            
        *   Draws the text line by line onto the image.
            
6.  **Error Handling:**
    
    *   The code has basic error handling (e.g., checking if the font file exists, handling image download errors). You might want to add more robust error handling for a production environment.
        
7.  **Font:**
    
    *   The code assumes you have arial.ttf in a location where Pillow can find it. You can change the font or use ImageFont.load\_default() if you don't have a specific font file.
        

**How to Run:**

1.  Save the code as a Python file (e.g., image\_text\_generator.py).
    
2.  Set the GOOGLE\_API\_KEY environment variable.
    
3.  python image\_text\_generator.pycontent\_copydownloadUse code [with caution](https://support.google.com/legal/answer/13505487).Bash
    

**Future Improvements:**

*   **Gemini Image API Integration:** Replace the placeholder image generation with the actual API when it's available.
    
*   **More Advanced Image Composition:** Explore more sophisticated image composition techniques in Pillow (e.g., layering, blending modes) to create visually appealing results.
    
*   **User Interface:** Consider creating a simple GUI (e.g., using Tkinter or a web framework) to make the tool more user-friendly.
    
*   **Error Handling:** Add more comprehensive error handling and input validation.
    
*   **Customization:** Allow the user to customize the font, colors, box size, etc.
    

This detailed code and explanation should give you a solid foundation for creating your automated image and text generation tool. Remember to adapt the image generation part when the Gemini image API becomes available. Please let me know if you have any other questions.
