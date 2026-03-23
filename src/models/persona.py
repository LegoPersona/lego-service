from pydantic import BaseModel


class Persona(BaseModel):
    beard: str
    eyebrows: str
    eyes: str
    hair: str
    nose: str
    pants: str
    shirt: str