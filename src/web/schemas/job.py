from typing import Optional

from pydantic import BaseModel, Field


class JobCreateSchema(BaseModel):
    """
    Схема создания вакансии
    """
    title: Optional[str] = Field(description="Название вакансии")
    description: Optional[str] = Field(description="Описание вакансии")
    salary_from: Optional[str] = Field(description="Нижний порог зарплаты")
    salary_to: Optional[str] = Field(description="Верхний порог зарплаты")
    is_active: bool = Field(default=True, description="Активность вакансии")


class JobSchema(JobCreateSchema):
    """
    Схема вакансии
    """
    id: int = Field(description="Идентификатор вакансии")
    user_id: int = Field(description="Идентификатор пользователя")


class JobUpdateSchema(JobCreateSchema):
    """
    Схема обновления вакансии
    """
    id: int = Field(description="Идентификатор вакансии")
