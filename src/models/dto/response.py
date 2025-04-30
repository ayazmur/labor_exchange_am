from pydantic import BaseModel, Field


class ResponseUpdateDto(BaseModel):
    """
    Модель для обновления откликов
    """
    message: str = Field(description="Письмо от пользователя")


class ResponseCreateDto(BaseModel):
    """
    Модель для создания откликов
    """
    job_id: int = Field(description="Идентификатор вакансии")
    user_id: int = Field(description="Идентификатор пользователя")
    message: str = Field(description="Письмо от пользователя")