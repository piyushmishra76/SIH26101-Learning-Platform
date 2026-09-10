from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

from app.Database.connection import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)

    filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)

    uploaded_by = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    status = Column(
        String(30),
        nullable=False,
        default="pending"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )