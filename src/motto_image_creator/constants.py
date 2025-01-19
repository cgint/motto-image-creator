import os
from pathlib import Path

PROJECT_ID = "gen-lang-client-0910640178"  # Replace with your project ID
LOCATION = "europe-west1"  # Replace with your location

api_key = os.getenv("GEMINI_API_KEY")
MODEL_POEM = "gemini-2.0-flash-exp" # "gemini-1.5-flash-latest"
MODEL_IMAGE_PROMPT = MODEL_POEM


MODEL_IMAGE_PROMPT_INCLUDE_POEM = False
USE_IMAGEN_3 = False
if USE_IMAGEN_3:
    MODEL_IMAGE_PROMPT_AVOID_PERSONS = True
    MODEL_IMAGE_GENERATE = "imagen-3.0-fast-generate-001"
    MODEL_IMAGE_PERSON_GENERATION = "dont_allow"
else:
    MODEL_IMAGE_PROMPT_AVOID_PERSONS = False
    MODEL_IMAGE_GENERATE = "imagegeneration@006"
    MODEL_IMAGE_PERSON_GENERATION = "allow_adults"

TEXT_FONT_PATH = "fonts/DejaVuSansMono-Bold.ttf"

output_dir = Path("output")

IMAGE_PROMPT_BY_POEM_CACHE_PATH = f"{output_dir}/image_prompt_by_poem_cache.json"
IMAGE_PROMPT_BY_POEM_CACHE_IGNORE = False

# MODEL_IMAGE_NEGATIVE_PROMPT = """
# nsfw, nudity, explicit content, gore, snuff, violence, blood, injury, mutilation,
# disfigurement, torture, abuse, self-harm, suicide, drugs, alcohol, smoking, weapons,
# hate symbols, offensive gestures, inappropriate behavior, child exploitation
# deformed limbs, mutation, extra fingers, missing arms, fused fingers,
# oversaturated, bad proportions, poorly rendered, low resolution, blurry image,
# watermark, signature, text, error, cropped, worst quality, jpeg artifacts,
# disfigured, gross proportions, malformed limbs, long neck, cloned face,
# unrealistic skin texture, asymmetrical features, disproportionate body parts,
# poorly composed, messy, cluttered, unprofessional, amateurish,
# distorted perspective, unnatural poses, awkward positioning,
# pixelated, noisy, glitchy, low-quality details,
# out of frame, cut off limbs, incomplete composition,
# cartoon-like, unrealistic lighting, unnatural colors
# """.strip().replace("\n", " ")

MODEL_IMAGE_NEGATIVE_PROMPT = "landscapes, mountains, oceans, rivers, lakes, forests, animals"