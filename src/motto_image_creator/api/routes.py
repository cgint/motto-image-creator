from fastapi import APIRouter, HTTPException
from datetime import datetime
from ..models.schemas import MottoRequest, MottoResponse
from ..services.ai_service import generate_poem, generate_image_prompt
from ..services.edit_image_service import add_text_to_image
from ..services.vertex_image_service import generate_image
from ..constants import output_dir, IMAGE_PROMPT_BY_POEM_CACHE_PATH, IMAGE_PROMPT_BY_POEM_CACHE_IGNORE, USE_IMAGEN_3
from ..file_backed_key_values_store import FileBackedKeyValuesStore
import json

router = APIRouter()

image_prompt_by_poem_cache = FileBackedKeyValuesStore(IMAGE_PROMPT_BY_POEM_CACHE_PATH)

@router.post("/generate", response_model=MottoResponse)
def generate_motto(request: MottoRequest) -> MottoResponse:
    try:
        user_input_type = request.type
        user_input = request.input.strip()
        if user_input_type == 'prompt':
            user_prompt = user_input
            print(f"Generating content for prompt: {user_prompt}")
            poem = generate_poem(user_prompt)
            print(f"Generated poem: {poem}")
        else:
            user_prompt = None
            poem = user_input
            print(f"Using provided poem: {poem}")
        
        if IMAGE_PROMPT_BY_POEM_CACHE_IGNORE or not image_prompt_by_poem_cache.contains(poem):
            print("Creating image prompt...")
            image_prompt = generate_image_prompt(user_prompt, poem)
            print("Generated image prompt. Content generation complete.")
            if not IMAGE_PROMPT_BY_POEM_CACHE_IGNORE:
                image_prompt_by_poem_cache.set(poem, image_prompt)
        else:
            print("Using cached image prompt.")
            image_prompt = image_prompt_by_poem_cache.get(poem)
        
        time_for_filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        
        # Generate the base image
        imagen_version = "3" if USE_IMAGEN_3 else "2"
        credits = f"Image by Google Imagen {imagen_version} ::: Text by Google Gemini ::: Prompt/Composition by me"
        image_extension="png"
        base_image_path = output_dir / f"base_{time_for_filename}"
        final_image_path = output_dir / f"motto_{time_for_filename}"
        input_prompt_path = output_dir / f"input_prompts_{time_for_filename}.json"

        # Save the input prompt to a file
        with open(input_prompt_path, "w") as f:
            f.write(json.dumps({
                "user_prompt": user_prompt,
                "poem": poem,
                "image_prompt": image_prompt,
                "credits": credits,
                "base_image_path": str(base_image_path),
                "final_image_path": str(final_image_path)
            }))

        base_image_filenames = generate_image(image_prompt, base_image_path, image_extension)
        print(f"Generated images: {len(base_image_filenames)}")
        
        # Add text to the generated image
        final_image_filenames = []
        for base_image_filename in base_image_filenames:
            final_image_path = base_image_filename.replace("base_", "motto_")
            add_text_to_image(base_image_filename, poem, credits, final_image_path)
            final_image_filenames.append(final_image_path)
        
        return MottoResponse(
            poem=poem,
            image_path_list=final_image_filenames
        )
    except Exception as e:
        import logging
        import traceback
        logging.error(f"Error generating motto: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))
