from pydantic import BaseModel
from src.models.persona import Persona


class InstructionsRequest(BaseModel):
    ldr_file: str

class PersonaRequest(BaseModel):
    persona: Persona