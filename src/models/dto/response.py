from pydantic import BaseModel


class ResponseUpdateDto(BaseModel):
    message: str


class ResponseCreateDto(BaseModel):
    job_id: int
    user_id: int
    message: str