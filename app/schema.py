import pydantic
from typing import Optional, Type
from abc import ABC

class AbstractAnnouncement(pydantic.BaseModel, ABC):
    title: str
    owner: str
    description: str

    @pydantic.field_validator("title")
    @classmethod
    def title_length(cls, v: str) -> str:
        if len(v) > 200:
            raise ValueError("Max length of title is 200")
        return v

    @pydantic.field_validator("owner")
    @classmethod
    def owner_length(cls, v: str) -> str:
        if len(v) > 100:
            raise ValueError("Max length of owner is 100")
        return v

class CreateAnnouncement(AbstractAnnouncement):
    title: str
    owner: str
    description: str

class UpdateAnnouncement(AbstractAnnouncement):
    title: Optional[str] = None
    description: Optional[str] = None
    owner: Optional[str] = None

SCHEMA_CLASS = Type[CreateAnnouncement | UpdateAnnouncement]
SCHEMA = CreateAnnouncement | UpdateAnnouncement