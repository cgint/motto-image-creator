# Motto Image Creator

A FastAPI service that generates motto images with AI-generated content using Google's Gemini API.

## Features

- Generates poems based on user prompts using Gemini Pro
- Creates images (placeholder for now, will use Gemini's image generation when available)
- Composites text onto images with stylized formatting
- 1024x1024 output images with rounded borders
- Semi-transparent text overlay

## Setup

1. Install dependencies:
```bash
poetry install
```

2. Set up environment variables:
```bash
export GEMINI_API_KEY=your_api_key_here
```

3. Run the server:
```bash
poetry run uvicorn src.motto_image_creator.main:app --reload
```

## API Usage

### Generate a Motto Image

```bash
curl -X POST "http://localhost:8000/api/generate" \
     -H "Content-Type: application/json" \
     -d '{"prompt": "creating user-centric software applications"}'
```

The response will include the generated poem and the path to the created image.

## Project Structure

```
motto-image-creator/
├── src/
│   └── motto_image_creator/
│       ├── api/
│       │   └── routes.py
│       ├── core/
│       ├── models/
│       │   └── schemas.py
│       ├── services/
│       │   ├── ai_service.py
│       │   └── image_service.py
│       └── main.py
├── tests/
├── pyproject.toml
└── README.md
```

## Future Improvements

- Integration with Gemini's image generation API when available
- Custom font support
- Additional styling options
- Image caching
- Background task processing for long-running generations
