from sqlalchemy import ForeignKey, text, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database import Base, str_uniq, int_pk, str_null_true
from datetime import date




class Note(Base):

    id: Mapped[int_pk]
    title: Mapped[str_uniq]
    content: Mapped[str_null_true]
    tags: Mapped[list["Tag"]] = relationship("Tag", back_populates="notes")

    def __str__(self):
        return f"<Note(id={self.id}, title={self.title})>"

    def __repr__(self):
        return str(self)

class Tag(Base):

    id: Mapped[int_pk]
    name: Mapped[str_uniq]

    notes: Mapped[list["Note"]] = relationship("Note", back_populates="tags")

    def __str__(self):
        return f"<Tag(id={self.id}, name={self.name})>"

    def __repr__(self):
        return str(self)
