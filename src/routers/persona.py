from fastapi import APIRouter
from src.models.persona import Persona
from src.services.persona import combine_modules


router = APIRouter(prefix="/persona", tags=["persona"])


@router.post("/generate")
def generate_persona(persona: Persona) -> dict:
    return {"ldr_file": combine_modules(persona)}