from typing import List, Annotated

from fastapi import Query


class RBNote:
    def __init__(self, note_id: int | None = None,
                 title: str | None = None,
                 tags: Annotated[List[str] | None, Query()] = None):
        self.id = note_id
        self.title = title
        self.tags = tags

    def to_dict(self) -> dict:
        data = {'id': self.id, 'title': self.title, 'tags': self.tags}
        # Создаем копию словаря, чтобы избежать изменения словаря во время итерации
        filtered_data = {key: value for key, value in data.items() if value is not None}
        return filtered_data