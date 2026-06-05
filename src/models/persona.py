from pydantic import BaseModel


class Module(BaseModel):
    file_name: str
    color: int


class Persona(BaseModel):
    pants: Module
    shirt: Module
    beard: Module
    nose: Module
    eyes: Module
    eyebrows: Module
    hair: Module
    skin_tone: int