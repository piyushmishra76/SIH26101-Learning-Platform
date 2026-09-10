from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
from pypdf import PdfReader
from sqlalchemy.orm import Session
from fastapi import Depends
from pydantic import BaseModel
from app.Database.connection import get_db
from app.models.document import Document
from app.utils.dependencies import get_current_user,get_current_trainer_or_admin
class DocumentStatusUpdate(BaseModel):
    status: str
router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


def extract_text_from_pdf(file_path):

    reader = PdfReader(file_path)

    pages = []

    for page in reader.pages:
        text = page.extract_text()

        if text:
            pages.append(text)

    return "\n".join(pages), len(reader.pages)

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is required"
        )

    allowed_extensions = {".pdf"}

    extension = Path(file.filename).suffix.lower()

    if extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported"
        )

    file_path = UPLOAD_DIR / file.filename

    contents = await file.read()

    with open(file_path, "wb") as buffer:
        buffer.write(contents)
    document = Document(
    filename=file.filename,
    file_path=str(file_path),
    uploaded_by=current_user.id,
    status="pending"
)

    db.add(document)
    db.commit()
    db.refresh(document)

    return {
    "message": "Document uploaded successfully",
    "document_id": document.id,
    "filename": document.filename,
    "uploaded_by": document.uploaded_by,
    "status": document.status,
    "created_at": document.created_at
}
@router.get("/")
def get_documents(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_trainer_or_admin)
):
    documents = db.query(Document).all()

    return documents
@router.post("/extract/{filename}")
def extract_pdf_text(filename: str):

    file_path = UPLOAD_DIR / filename

    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail="PDF file not found"
        )

    if file_path.suffix.lower() != ".pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported"
        )

    reader = PdfReader(file_path)

    pages = []

    for page in reader.pages:
        text = page.extract_text()

        if text:
            pages.append(text)

    full_text = "\n".join(pages)

    return {
        "filename": filename,
        "total_pages": len(reader.pages),
        "text": full_text
    }
@router.patch("/{document_id}/status")
def update_document_status(
    document_id: int,
    request: DocumentStatusUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_trainer_or_admin)
):
    if request.status not in {"approved", "rejected"}:
        raise HTTPException(
            status_code=400,
            detail="Status must be approved or rejected"
        )

    document = (
        db.query(Document)
        .filter(Document.id == document_id)
        .first()
    )

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    document.status = request.status

    db.commit()
    db.refresh(document)

    return {
        "message": f"Document {request.status} successfully",
        "document_id": document.id,
        "status": document.status
    }