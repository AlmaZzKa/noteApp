from fastapi import APIRouter, Depends
from app.notes.dao import NoteDAO
from app.notes.schemas import SNote, SNoteAdd
from app.notes.rb import RBNote

router = APIRouter(prefix='/notes', tags=['Работа с заметками'])

@router.get("/", summary="Получить все заметки")
async def get_students_by_query(request_body: RBNote = Depends()) -> list[SNote]:
    return await NoteDAO.find_by_query(**request_body.to_dict())

@router.post("/", summary="Создать новую заметку")
async def create_note(note: SNoteAdd) -> dict:
    check = await NoteDAO.create(note.dict())  # Преобразуем SNote в dict для использования в DAO.create(note)))
    if check:
        return {"message": "Заметка успешно создана!", "note": note}
    else:
        return {"message": "Ошибка при создании заметки!"}

@router.delete("/{note_id}", summary="Удалить заметку")
async def delete_note(note_id: int) -> dict:
    check = await NoteDAO.delete(note_id)
    if check:
        return {"message": f"Заметка с ID {note_id} удалена!"}
    else:
        return {"message": "Ошибка при удалении заметки!"}

@router.put("/{note_id}", summary="Обновить заметку")
async def update_note(note_id: int, note: SNoteAdd) -> dict:
    check = await NoteDAO.update(note_id, note.dict())
    if check:
        return {"message": "Заметка успешно изменена!", "note": note}
    else:
        return {"message": "Ошибка при изменении заметки!"}


@router.patch("/{note_id}/tags", summary="Добавить/удалить теги у заметки")
async def patch_note_tags(note_id: int, tags: list[str]) -> dict:
    check = await NoteDAO.patch_tags(note_id, tags)
    if check:
        return {"message": "Теги у заметки успешно изменены!", "tags": tags}
    else:
        return {"message": "Ошибка при изменении тегов заметки!"}
