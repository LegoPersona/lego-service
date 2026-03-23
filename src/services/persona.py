from pathlib import Path

from src.models.persona import Persona


TEMPLATE_ROOT = Path(__file__).resolve().parents[2] / "templates"


def combine_modules(persona: Persona) -> str:
	combined = ""

	base_file = TEMPLATE_ROOT / "head-base.ldr"
	combined += base_file.read_text(encoding="utf-8") + "\n"

	for key, value in persona.model_dump().items():
		file_path = TEMPLATE_ROOT / key / f"{value}.ldr"
		combined += file_path.read_text(encoding="utf-8") + "\n"

	return combined
