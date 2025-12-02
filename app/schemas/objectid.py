from typing import Any, Callable, Iterator

from bson import ObjectId
from pydantic import GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue


class PyObjectId(ObjectId):
    """
    Custom ObjectId type that works with Pydantic v2
    """

    @classmethod
    def __get_validators__(cls) -> Iterator[Callable[[Any], Any]]:
        yield cls.validate

    @classmethod
    def validate(cls, v: Any) -> ObjectId:
        if isinstance(v, ObjectId):
            return v
        if not ObjectId.is_valid(v):
            raise ValueError(f"Invalid ObjectId: {v}")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(
        cls,
        core_schema: dict,
        handler: GetJsonSchemaHandler,
    ) -> JsonSchemaValue:
        """
        Pydantic v2에서 JSON Schema를 커스텀하는 공식 메서드
        (v1의 __modify_schema__ 대체)
        """
        json_schema = handler(core_schema)
        json_schema.update(type="string")
        return json_schema
