from typing import Optional

from pydantic import BaseModel, Field


class ResponseSchema(BaseModel):
    """
    Схема отклика
    """
    id: Optional[int] = Field(description="Идентификатор отклика")
    job_id: int = Field(description="Идентификатор вакансии")
    user_id: int = Field(description="Идентификатор пользователя")
    message: str = Field(description="Письмо от пользователя ")


class ResponseUpdateSchema(BaseModel):
    """
    Схема обновления вакансии
    """
    job_id: int = Field(description="Идентификатор вакансии")
    user_id: int = Field(description="Идентификатор пользователя")
    message: str = Field(description="Письмо от пользователя ")


class ResponseCreateSchema(BaseModel):
    """
    Схема создания отклика
    """
    id: Optional[int] = Field(description="идентифкатор отклика")
    job_id: int = Field(description="Идентификатор вакансии")
    user_id: int = Field(description="Идентификатор пользователя")
    message: str = Field(description="Письмо от пользователя ")
