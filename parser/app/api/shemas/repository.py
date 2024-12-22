from pydantic import BaseModel, Field


class RepositoryModel(BaseModel):
    repo: str = Field(examples=["Stellarium"], description="full_name из API github")
    owner: str = Field(examples=["Stellarium"], description="Владелец репозитория")
    position_cur: int = Field(examples=[1], description="Текущая позиция в топе")
    position_prev: int | None = Field(examples=[3], description="Позиция в топе до последнего обновления")
    stars: int = Field(examples=[], description="")
    watchers: int = Field(
        examples=[550],
        description="количество пользователей, подписавшихся на уведомления о изменениях"
    )
    forks: int = Field(examples=[20])
    open_issues: int = Field(examples=[50])
    language: str | None = Field(examples=["python"])

