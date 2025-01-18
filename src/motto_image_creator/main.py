from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
from .api.routes import router
from .services.vertex_image_service import init_vertex
from .services.gemini_image_service import init_genai

app = FastAPI(
    title="Motto Image Creator",
    description="A service for creating motto images with AI-generated content",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
static_path = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=str(static_path)), name="static")

# Mount output directory for generated images
output_path = Path("output")
output_path.mkdir(exist_ok=True)
app.mount("/output", StaticFiles(directory=str(output_path)), name="output")

# Initialize Gemini AI on startup
@app.on_event("startup")
async def startup_event():
    init_genai()
    init_vertex()
# Include routers
app.include_router(router, prefix="/api")

# Serve index.html at root
@app.get("/")
async def serve_index():
    return FileResponse(str(static_path / "index.html"))

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}
