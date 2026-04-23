import subprocess
import uuid
from pathlib import Path

from src.models.persona import Persona


TEMPLATE_ROOT = Path(__file__).resolve().parents[2] / "templates"


def combine_modules(persona: Persona) -> str:
	combined = ""

	base_file = TEMPLATE_ROOT / "head-base.ldr"
	combined += base_file.read_text(encoding="utf-8") + "\n"

	for key, value in persona.model_dump().items():
		file_path = TEMPLATE_ROOT / key / f"{value}.ldr"
		combined += "0 STEP\n" + file_path.read_text(encoding="utf-8") + "\n"

	return combined


def generate_instructions(ldr_file: str) -> Path:
	job_id = uuid.uuid4()
	tmp_dir = Path("/tmp") / str(job_id)
	tmp_dir.mkdir(parents=True, exist_ok=True)

	ldr_path = tmp_dir / "model.ldr"
	ldr_path.write_text(ldr_file, encoding="utf-8")

	pdf_path = tmp_dir / "instructions.pdf"

	cmd = [
		"xvfb-run", "-a",
		"env",
		"QT_OPENGL=software",
		"LIBGL_ALWAYS_SOFTWARE=1",
		"lpub3d24",
		"-of", str(pdf_path),
		"-pe", "pdf",
		str(ldr_path),
	]
	subprocess.run(cmd, check=True)

	return pdf_path

