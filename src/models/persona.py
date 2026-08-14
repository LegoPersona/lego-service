from pydantic import BaseModel


class Module(BaseModel):
    file_name: str
    color: int
    secondary_color: int | None = None


class Persona(BaseModel):
    pants: Module
    shirt: Module
    beard: Module
    nose: Module
    eyes: Module
    eyebrows: Module
    glasses: Module
    hair: Module
    skin_tone: int