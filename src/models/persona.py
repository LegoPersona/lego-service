from pydantic import BaseModel


class Persona(BaseModel):
    pants: str
    shirt: str
    beard: str
    nose: str
    eyes: str
    eyebrows: str
    hair: str