from typing import Optional

from pydantic import BaseModel, Field


class JobUpdateDto(BaseModel):
    """
    Модель данных для обновления вакансии
    """
    title: Optional[str] = Field(description="Название вакансии")
    description: Optional[str] = Field(description="Описание вакансии")
    salary_from: Optional[str] = Field(description="Нижний порог зарплаты")
    salary_to: Optional[str] = Field(description="Верхний порог зарплаты")
    is_active: bool = Field(description="Активность вакансии")


class JobCreateDto(JobUpdateDto):
    """
    Модель данных для создания вакансии
    """
    user_id: int = Field(description="ID пользователя, создающего вакансию")