# PDF Backend — Module 1 (Conversion)

This module provides a FastAPI backend that converts PDF -> DOCX/PPTX/XLSX using LibreOffice.

## Endpoints
- POST /convert/pdf-to-word
- POST /convert/pdf-to-ppt
- POST /convert/pdf-to-excel
- GET  /download/{filename}
- GET  /health

## Deploy
Recommended: deploy via Render using Docker (Dockerfile present).

## Local dev
Install libreoffice locally if testing outside Docker.
Run:
`uvicorn main:app --reload --host 0.0.0.0 --port 8000`
