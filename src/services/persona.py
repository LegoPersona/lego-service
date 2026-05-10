import subprocess
import uuid
from pathlib import Path

from src.models.persona import Persona


TEMPLATE_ROOT = Path(__file__).resolve().parents[2] / "templates"


def _apply_color(content: str, color: int) -> str:
	lines = []
	for line in content.splitlines():
		words = line.split()
		if len(words) >= 2 and words[1] == "0":
			words[1] = str(color)
			line = " ".join(words)
		lines.append(line)
	return "\n".join(lines)


def combine_modules(persona: Persona) -> str:
	combined = (TEMPLATE_ROOT / "file-base.ldr").read_text(encoding="utf-8") + "\n"

	for key, module in persona:
		file_path = TEMPLATE_ROOT / key / module.file_name
		content = _apply_color(file_path.read_text(encoding="utf-8"), module.color)
		combined += "0 STEP\n" + content + "\n"
		if key == "shirt":
			combined += "0 STEP\n" + (TEMPLATE_ROOT / "head-base.ldr").read_text(encoding="utf-8") + "\n"

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


def generate_image(ldr_file: str) -> Path:
	job_id = uuid.uuid4()
	tmp_dir = Path("/tmp") / str(job_id)
	tmp_dir.mkdir(parents=True, exist_ok=True)

	ldr_path = tmp_dir / "model.ldr"
	ldr_path.write_text(ldr_file, encoding="utf-8")

	cmd = [
		"xvfb-run", "-a",
		"env",
		"QT_OPENGL=software",
		"LIBGL_ALWAYS_SOFTWARE=1",
		"lpub3d24",
		"-pf",
		str(ldr_path),
	]
	subprocess.run(cmd, check=True)

	pngs = sorted(tmp_dir.glob("**/assem/*.png"))
	if not pngs:
		raise RuntimeError("lpub3d24 produced no PNG output")
	return pngs[-1]

