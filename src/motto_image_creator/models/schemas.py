from pydantic import BaseModel, Field

class MottoRequest(BaseModel):
    prompt: str = Field(..., description="The prompt for generating the poem and image")

class MottoResponse(BaseModel):
    poem: str = Field(..., description="The generated poem")
    image_path: str = Field(..., description="Path to the generated image")
