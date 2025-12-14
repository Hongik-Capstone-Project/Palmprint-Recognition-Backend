from typing import Generic, List, Type, TypeVar

from beanie import Document

ModelType = TypeVar("ModelType", bound=Document)


class BaseOdmRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get_by_id(self, id):
        return await self.model.get(id)

    async def find_all(self) -> List[ModelType]:
        return await self.model.find_all().to_list()

    async def find(self, *args, **kwargs) -> List[ModelType]:
        return await self.model.find(*args, **kwargs).to_list()

    async def create(self, obj: ModelType) -> ModelType:
        await obj.insert()
        return obj

    async def update(self, obj: ModelType) -> ModelType:
        await obj.save()
        return obj

    async def delete(self, obj: ModelType):
        await obj.delete()
