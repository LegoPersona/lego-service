from fastapi import FastAPI
from src.routers.persona import router as persona_router


app = FastAPI(title="Lego Service API")

app.include_router(persona_router)
