from pydantic import BaseModel, Field

class MottoRequest(BaseModel):
    input: str = Field(..., description="The prompt for generating the poem and image")
    type: str = Field(..., description="The type of request, either 'prompt' or 'poem'")

class MottoResponse(BaseModel):
    poem: str = Field(..., description="The generated poem")
    image_path_list: list[str] = Field(..., description="Paths to the generated images")