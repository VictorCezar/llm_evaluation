import os
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from app.api.endpoints import router as api_router

app = FastAPI(
    title="LLM-as-a-Judge API",
    version="1.0.0",
    description="Sistema de avaliação de conversas de atendimento com Microsoft Presidio e Groq (Instructor)."
)

# Enable CORS for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include endpoints router
app.include_router(api_router)

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serves the dashboard frontend page."""
    template_path = os.path.join(os.path.dirname(__file__), "templates", "index.html")
    if not os.path.exists(template_path):
        return HTMLResponse(
            content="<h1>Template não encontrado</h1><p>Verifique se o arquivo index.html existe em app/templates/.</p>",
            status_code=status.HTTP_404_NOT_FOUND
        )
    with open(template_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

@app.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    """Simple health check endpoint."""
    return {"status": "healthy"}

