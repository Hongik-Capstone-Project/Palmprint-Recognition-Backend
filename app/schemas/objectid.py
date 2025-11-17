# app/schemas/objectid.py (수정)

from typing import Any, Callable, Iterator # 💡 Iterator 추가
from bson import ObjectId

# BSON 라이브러리의 ObjectId 타입을 Pydantic에서 처리할 수 있도록 설정
class PyObjectId(ObjectId):
    
    # @classmethod
    # def __get_validators__(cls) -> Callable: # ❌ 이 부분을 수정합니다.
    @classmethod
    # 💡 반환 타입을 제너레이터(Iterator)로 명확히 지정
    def __get_validators__(cls) -> Iterator[Callable[[Any], Any]]:
        yield cls.validate

    @classmethod
    def validate(cls, v: Any) -> ObjectId:
        if not ObjectId.is_valid(v):
            raise ValueError(f"Invalid ObjectId: {v}")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema: dict) -> None:
        field_schema.update(type="string")