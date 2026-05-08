from fastapi import APIRouter, BackgroundTasks
from fastapi.responses import FileResponse
from src.models.requests import InstructionsRequest, PersonaRequest
from src.models.persona import Persona
import shutil
from src.services.persona import combine_modules, generate_instructions, generate_image


router = APIRouter(prefix="/persona", tags=["persona"])


@router.post("/generate")
def generate_persona(request: PersonaRequest) -> dict:
    return {"ldr_file": combine_modules(request.persona)}

@router.post("/instructions")
def generate_instructions_route(request: InstructionsRequest, background_tasks: BackgroundTasks):
    pdf_path = generate_instructions(request.ldr_file)
    background_tasks.add_task(shutil.rmtree, pdf_path.parent)
    return FileResponse(
        path=pdf_path,
        media_type="application/pdf",
        filename="instructions.pdf",
    )

@router.post("/image")
def generate_image_route(request: InstructionsRequest, background_tasks: BackgroundTasks):
    png_path = generate_image(request.ldr_file)
    background_tasks.add_task(shutil.rmtree, png_path.parent)
    return FileResponse(
        path=png_path,
        media_type="image/png",
        filename="model.png",
    )