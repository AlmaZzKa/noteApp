from sqlalchemy import select, delete
from sqlalchemy.orm import joinedload

from app.database import async_session_maker
from app.dao.base import BaseDAO
from app.notes.models import Note, Tag, note_tag_association


class NoteDAO(BaseDAO):
    model = Note

    @classmethod
    async def find_by_query(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(Note).options(joinedload(cls.model.tags))


            if 'id' in filter_by and filter_by['id']:
                query = query.filter(Note.id == filter_by['id'])

            if 'title' in filter_by and filter_by['title']:
                query = query.filter(Note.title.ilike(f"%{filter_by['title']}%"))

            # Проверяем наличие tags в filter_by
            if 'tags' in filter_by and filter_by['tags']:
                tags = [tag.lower() for tag in filter_by['tags']]
                query = query.join(Note.tags).filter(Tag.name.in_(tags))

            result = await session.execute(query)
            notes = result.unique().scalars().all()
            notes = [{"id": note.id, "title": note.title, "content": note.content, "tags": [tag.name for tag in note.tags]} for note in notes]
            return notes



    @classmethod
    async def create(cls, note: dict):
        async with async_session_maker() as session:
            async with session.begin():

                # Обрабатываем теги
                tags = note.get("tags", [])
                existing_tags = []

                for tag_name in tags:
                    # Ищем существующий тег
                    result = await session.execute(select(Tag).where(Tag.name == tag_name.lower()))
                    tag = result.scalars().first()

                    if tag:
                        existing_tags.append(tag)
                    else:
                        # Если тег не существует, создаем новый
                        new_tag = Tag(name=tag_name.lower())
                        session.add(new_tag)
                        await session.flush()
                        existing_tags.append(new_tag)


                # Добавляем теги к заметке
                note['tags'] = existing_tags
                new_note = Note(**note)
                session.add(new_note)

                await session.commit()
                return new_note.id

    @classmethod
    async def delete(cls, note_id: int):
        async with async_session_maker() as session:
            async with session.begin():
                # Поиск заметки по ID
                query = select(cls.model).options.filter_by(id=note_id)
                result = await session.execute(query)
                note_to_delete = result.scalar_one_or_none()

                if not note_to_delete:
                    return None

                # Сначала удаляем связанные записи в note_tag
                await session.execute(
                    delete(note_tag_association).where(note_tag_association.c.note_id == note_id)
                )

                # Затем удаляем заметку из notes
                await session.execute(
                    delete(cls.model).filter_by(id=note_id)
                )

                await session.commit()
                return note_id

    @classmethod
    async def update(cls, note_id: int, note: dict):
        async with async_session_maker() as session:
            async with session.begin():
                # Поиск заметки по ID
                query = select(cls.model).options(joinedload(cls.model.tags)).filter_by(id=note_id)
                result = await session.execute(query)
                note_to_update = result.unique().scalar_one_or_none()

                if not note_to_update:
                    return None  # Если заметка не найдена

                # Обновляем поля заметки
                note_to_update.title = note.get("title", note_to_update.title)
                note_to_update.content = note.get("content", note_to_update.content)


                # Работа с тегами
                tags = note.get("tags", [])  # Получаем список тегов из переданных данных
                new_tags = set()

                for tag_name in tags:
                    # Ищем существующий тег
                    tag_result = await session.execute(select(Tag).where(Tag.name == tag_name.lower()))
                    tag = tag_result.scalars().first()

                    if tag:
                        new_tags.add(tag)
                    else:
                        # Если тег не существует, создаем новый
                        new_tag = Tag(name=tag_name.lower())
                        session.add(new_tag)
                        await session.flush()  # Фиксируем создание нового тега, чтобы получить его ID
                        new_tags.add(new_tag)

                # Удаляем старые теги, которые не нужны
                for tag in note_to_update.tags:
                    if tag.name not in new_tags:
                        note_to_update.tags.remove(tag)

                # Добавляем новые теги к заметке
                for tag in new_tags:
                    if tag not in note_to_update.tags:
                        note_to_update.tags.append(tag)

                # Фиксируем изменения
                await session.commit()

                return note_to_update  # Возвращаем обновленную заметку

    @classmethod
    async def patch_tags(cls, note_id: int, tags: list[str]):
        async with async_session_maker() as session:
            async with session.begin():
                # Поиск заметки по ID
                query = select(cls.model).options(joinedload(cls.model.tags)).filter_by(id=note_id)
                result = await session.execute(query)
                note_to_update = result.unique().scalar_one_or_none()

                if not note_to_update:
                    return None  # Если заметка не найдена

                # Приводим теги к нижнему регистру для единообразия
                tags_lower = [tag.lower() for tag in tags]

                # Работа с новыми тегами
                new_tags = set()

                for tag_name in tags_lower:
                    # Ищем существующий тег
                    tag_result = await session.execute(select(Tag).where(Tag.name == tag_name))
                    tag = tag_result.scalars().first()

                    if tag:
                        new_tags.add(tag)
                    else:
                        # Если тег не существует, создаем новый
                        new_tag = Tag(name=tag_name)
                        session.add(new_tag)
                        await session.flush()  # Фиксируем создание нового тега, чтобы получить его ID
                        new_tags.add(new_tag)

                # Удаляем старые теги, которые не нужны
                for tag in note_to_update.tags:
                    if tag.name not in new_tags:
                        note_to_update.tags.remove(tag)

                # Добавляем новые теги к заметке
                for tag in new_tags:
                    if tag not in note_to_update.tags:
                        note_to_update.tags.append(tag)

                # Фиксируем изменения
                await session.commit()

                return note_to_update  # Возвращаем обновленную заметку









