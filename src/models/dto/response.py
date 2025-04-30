from pydantic import BaseModel, Field


class ResponseUpdateDto(BaseModel):
    message: str


class ResponseCreateDto(BaseModel):
    job_id: int = Field()
    user_id: int
    message: str