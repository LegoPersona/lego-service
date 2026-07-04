import subprocess
import uuid
from pathlib import Path

from src.models.persona import Persona


TEMPLATE_ROOT = Path(__file__).resolve().parents[2] / "templates"

# (x_tilt, y_spin) for ROTSTEP x_tilt y_spin 0 ABS.
# x_tilt=30 gives natural depth. Each y_spin has +30° added so no view is dead-flat:
#   front 30° (slight right-diagonal), right 120° (right+back perspective),
#   left -120° (symmetric mirror of right), back 210° (back+right perspective).
DIRECTION_ROT = {
	"front": (30,   30),
	"right": (30,  120),
	"left":  (30, -120),
	"back":  (30,  210),
}


def _classify_direction(x: float, z: float) -> str:
	abs_x, abs_z = abs(x), abs(z)
	if abs_x < 15 and abs_z < 15:
		return "front"
	if abs_z >= abs_x:
		return "front" if z <= 0 else "back"
	return "left" if x < 0 else "right"


def _ldr_to_directional_steps(content: str) -> str:
	"""Emit parts in original order; insert a ROTSTEP+STEP boundary each time the
	viewing direction changes so every part is visible without reordering."""
	current_dir: str | None = None
	pending: list[str] = []
	result = ""

	for line in content.splitlines():
		stripped = line.strip()
		if not stripped:
			continue
		tokens = stripped.split()
		if tokens[0] != "1":
			continue
		x, z = float(tokens[2]), float(tokens[4])
		direction = _classify_direction(x, z)

		if direction != current_dir:
			if pending:
				x_tilt, y_spin = DIRECTION_ROT[current_dir]
				for i in range(0, len(pending), 5):
					chunk = pending[i:i + 5]
					result += "\n".join(chunk) + "\n"
					result += f"0 ROTSTEP {x_tilt} {y_spin} 0 ABS\n"
					result += "0 STEP\n"
				pending = []
			current_dir = direction

		pending.append(line)

	if pending and current_dir is not None:
		x_tilt, y_spin = DIRECTION_ROT[current_dir]
		for i in range(0, len(pending), 5):
			chunk = pending[i:i + 5]
			result += "\n".join(chunk) + "\n"
			result += f"0 ROTSTEP {x_tilt} {y_spin} 0 ABS\n"
			result += "0 STEP\n"

	return result


def _apply_color(content: str, color: int, replace: str) -> str:
	lines = []
	for line in content.splitlines():
		words = line.split()
		if len(words) >= 2 and words[1] == replace:
			words[1] = str(color)
			line = " ".join(words)
		lines.append(line)
	return "\n".join(lines)


def combine_modules(persona: Persona) -> str:
	combined = (TEMPLATE_ROOT / "file-base.ldr").read_text(encoding="utf-8") + "\n"

	for key, module in persona:
		if key != "skin_tone":
			file_path = TEMPLATE_ROOT / key / module.file_name
			content = _apply_color(file_path.read_text(encoding="utf-8"), module.color, replace="0")
			combined += _ldr_to_directional_steps(content)
			if key == "beard":
				combined += _ldr_to_directional_steps(
					(TEMPLATE_ROOT / "head-base.ldr").read_text(encoding="utf-8")
				)
	
	combined = _apply_color(combined, persona.skin_tone, replace="SKIN")

	combined += "0 ROTSTEP 30 30 0 ABS\n"
	combined += "0 STEP\n"

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


def _assemble_ldr(ldr_content: str) -> str:
	"""Strip all step/rotstep markers and render as one completed-model view."""
	lines = [
		line for line in ldr_content.splitlines()
		if not line.strip().startswith(("0 STEP", "0 ROTSTEP"))
	]
	return "\n".join(lines) + "\n"


def generate_image(ldr_file: str) -> Path:
	job_id = uuid.uuid4()
	tmp_dir = Path("/tmp") / str(job_id)
	tmp_dir.mkdir(parents=True, exist_ok=True)

	ldr_path = tmp_dir / "model.ldr"
	ldr_path.write_text(_assemble_ldr(ldr_file), encoding="utf-8")

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

	pngs = sorted(tmp_dir.glob("**/assem/*.png"), key=lambda p: p.stat().st_mtime)
	if not pngs:
		raise RuntimeError("lpub3d24 produced no PNG output")
	return pngs[-1]

def generate_parts_csv(ldr_file: str) -> Path:
	job_id = uuid.uuid4()
	tmp_dir = Path("/tmp") / str(job_id)
	tmp_dir.mkdir(parents=True, exist_ok=True)

	ldr_path = tmp_dir / "model.ldr"
	ldr_path.write_text(ldr_file, encoding="utf-8")

	csv_path = tmp_dir / "model-export.csv"

	cmd = [
		"xvfb-run", "-a",
		"env",
		"QT_OPENGL=software",
		"LIBGL_ALWAYS_SOFTWARE=1",
		"lpub3d24",
		"-pe",
		"-o", "csv",
		str(ldr_path),
	]
	subprocess.run(cmd, check=True)

	return csv_path

