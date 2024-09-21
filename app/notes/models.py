from sqlalchemy import ForeignKey, Column, Table
from sqlalchemy.orm import relationship, Mapped
from app.database import Base, str_uniq, int_pk, str_null_true
from datetime import date
from sqlalchemy import event


note_tag_association = Table( # связующая таблица для связи заметок и тегов
    "note_tag", Base.metadata,
Column("note_id", ForeignKey("notes.id"), primary_key=True, nullable=False),
Column("tag_id", ForeignKey("tags.id"), primary_key=True, nullable=False)


)

class Note(Base):

    id: Mapped[int_pk]
    title: Mapped[str_null_true]
    content: Mapped[str_null_true]
    user_id: Mapped[int] = Column(ForeignKey("users.id"))

    tags: Mapped[list["Tag"]] = relationship("Tag", secondary=note_tag_association, back_populates="notes")

    def __str__(self):
        return f"<Note(id={self.id}, title={self.title})>"

    def __repr__(self):
        return str(self)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "tags": [tag.id for tag in self.tags]  # возвращаем список ID тегов
        }

class Tag(Base):

    id: Mapped[int_pk]
    name: Mapped[str_uniq]

    notes: Mapped[list["Note"]] = relationship("Note", secondary=note_tag_association, back_populates="tags")

    def __str__(self):
        return f"<Tag(id={self.id}, name={self.name})>"

    def __repr__(self):
        return str(self)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "notes": [note.id for note in self.notes]  # возвращаем список ID заметок
        }

@event.listens_for(Tag, "before_insert")
def receive_before_insert(mapper, connection, target):
    target.name = target.name.lower()


