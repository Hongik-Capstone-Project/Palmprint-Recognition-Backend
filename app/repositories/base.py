from typing import Any, Generic, TypeVar

from sqlalchemy import select

from app.models.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    def __init__(self, model: type[ModelType]):
        self.model = model

    def get_query(self):
        return select(self.model)

    def get_by_id_query(self, id: int):
        return select(self.model).where(self.model.id == id)

    def search_query(self, column: Any, keyword: str):
        return select(self.model).where(column.like(f"%{keyword}%"))

    def exact_query(self, column: Any, value: Any):
        return select(self.model).where(column == value)
