from pathlib import Path

root_dir = Path(__file__).resolve().parent

def resolve_icon(file_name):
	return str(root_dir / 'icons' / file_name)