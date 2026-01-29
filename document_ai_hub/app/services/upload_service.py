from sqlalchemy.orm import Session
from app.database.model import DocumentMetaData


def create_doc(db: Session, document_name: str, file_domain: str, uploaded_by: str):
    new_doc = DocumentMetaData(
        document_name=document_name,
        file_domain=file_domain,
        uploaded_by=uploaded_by
    )
    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)
    return new_doc