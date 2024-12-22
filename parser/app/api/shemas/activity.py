from datetime import date

from pydantic import BaseModel, Field


class ActivityModel(BaseModel):
    commits: int = Field(examples=[2200], description="количество коммитов за день")
    authors: list[str] = Field(examples=[["Taylor Waggoner", "Shellea Williams"]])
    date: date


class ActivityOut(BaseModel):
    items: list[ActivityModel]
    count: int = Field(examples=[1], description="количество всех записей, соответствующих запросу")

