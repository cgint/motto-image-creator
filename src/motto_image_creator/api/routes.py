from fastapi import APIRouter, HTTPException
from pathlib import Path
from ..models.schemas import MottoRequest, MottoResponse
from ..services.ai_service import generate_content
from ..services.gemini_image_service import add_text_to_image, generate_image

router = APIRouter()

@router.post("/generate", response_model=MottoResponse)
def generate_motto(request: MottoRequest) -> MottoResponse:
    try:
        # Generate poem and image prompt
        poem, image_prompt = generate_content(request.prompt)
        
        # Set up output directory
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        
        # Generate the base image
        base_image_path = output_dir / "base.png"
        generate_image(image_prompt, base_image_path)
        
        # Add text to the generated image
        final_image_path = output_dir / "motto.png"
        final_image_path = add_text_to_image(base_image_path, poem, final_image_path)
        
        return MottoResponse(
            poem=poem,
            image_path=str(final_image_path)
        )
    except Exception as e:
        import logging
        import traceback
        logging.error(f"Error generating motto: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))
