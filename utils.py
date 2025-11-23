# utils.py
import os
import uuid

UPLOAD_DIR = os.environ.get("UPLOAD_DIR", "/app/uploads")
ALLOWED_EXTENSIONS = {".pdf"}

def ensure_dirs():
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    os.makedirs(os.environ.get("OUTPUT_DIR", "/app/converted"), exist_ok=True)

def save_upload_file(upload_file, prefix: str = "") -> str:
    """
    Save fastapi UploadFile to disk, return full path.
    """
    ext = os.path.splitext(upload_file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        # allow only pdf here
        raise ValueError("Only PDF uploads allowed for this endpoint")
    fname = f"{prefix}{uuid.uuid4().hex}{ext}"
    out_path = os.path.join(UPLOAD_DIR, fname)
    with open(out_path, "wb") as out:
        while True:
            chunk = upload_file.file.read(1024 * 1024)
            if not chunk:
                break
            out.write(chunk)
    return out_path
