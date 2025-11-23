# main.py
import os
import shutil
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from converters.pdf_to_office import convert_pdf_to_format
from utils import ensure_dirs, save_upload_file

UPLOAD_DIR = os.environ.get("UPLOAD_DIR", "/app/uploads")
OUTPUT_DIR = os.environ.get("OUTPUT_DIR", "/app/converted")
MAX_FILE_SIZE = int(os.environ.get("MAX_FILE_SIZE", 50 * 1024 * 1024))  # 50MB default

ensure_dirs()

app = FastAPI(title="PDF Converter API - Module 1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ConvertResponse(BaseModel):
    filename: str
    format: str
    size: int

@app.get("/health")
def health():
    return {"status": "ok"}

def validate_file(file: UploadFile):
    if file.content_type not in ("application/pdf", "application/octet-stream"):
        raise HTTPException(status_code=400, detail="Uploaded file must be a PDF")

@app.post("/convert/pdf-to-word", response_model=ConvertResponse)
async def pdf_to_word(file: UploadFile = File(...)):
    validate_file(file)
    try:
        saved = save_upload_file(file, prefix="pdf2word_")
        out_path = convert_pdf_to_format(saved, "docx")
        stat = os.stat(out_path)
        return ConvertResponse(filename=os.path.basename(out_path), format="docx", size=stat.st_size)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/convert/pdf-to-ppt", response_model=ConvertResponse)
async def pdf_to_ppt(file: UploadFile = File(...)):
    validate_file(file)
    try:
        saved = save_upload_file(file, prefix="pdf2ppt_")
        out_path = convert_pdf_to_format(saved, "pptx")
        stat = os.stat(out_path)
        return ConvertResponse(filename=os.path.basename(out_path), format="pptx", size=stat.st_size)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/convert/pdf-to-excel", response_model=ConvertResponse)
async def pdf_to_excel(file: UploadFile = File(...)):
    validate_file(file)
    try:
        saved = save_upload_file(file, prefix="pdf2excel_")
        out_path = convert_pdf_to_format(saved, "xlsx")
        stat = os.stat(out_path)
        return ConvertResponse(filename=os.path.basename(out_path), format="xlsx", size=stat.st_size)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/download/{filename}")
def download(filename: str):
    path = os.path.join(OUTPUT_DIR, filename)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path, media_type="application/octet-stream", filename=filename)
