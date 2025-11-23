# converters/pdf_to_office.py
import os
import subprocess
from typing import Tuple

OUTPUT_DIR = os.environ.get("OUTPUT_DIR", "/app/converted")

def convert_pdf_to_format(input_path: str, output_format: str, timeout:int=120) -> str:
    """
    Convert input_path PDF to output_format (like 'docx', 'pptx', 'xlsx') using LibreOffice CLI.
    Returns the full path to the converted file in OUTPUT_DIR.
    Raises RuntimeError on failure.
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError("Input file not found")

    cmd = [
        "libreoffice",
        "--headless",
        "--convert-to", output_format,
        "--outdir", OUTPUT_DIR,
        input_path
    ]

    # Run conversion
    try:
        subprocess.run(cmd, check=True, timeout=timeout)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"LibreOffice conversion failed: {e}")
    except subprocess.TimeoutExpired:
        raise RuntimeError("LibreOffice conversion timed out")

    base = os.path.splitext(os.path.basename(input_path))[0]
    expected = os.path.join(OUTPUT_DIR, f"{base}.{output_format}")

    # In some cases libreoffice changes case or adds suffix - search fallback
    if os.path.exists(expected):
        return expected

    for f in os.listdir(OUTPUT_DIR):
        if f.startswith(base) and f.lower().endswith(output_format.lower()):
            return os.path.join(OUTPUT_DIR, f)

    raise RuntimeError("Converted file not found after conversion")
