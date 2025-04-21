from typing import Optional

from pydantic import BaseModel, EmailStr, constr, model_validator
from typing_extensions import Self
# id: int
#     job_id: int
#     user_id: int
#     message: str

class ResponseSchema(BaseModel):
    id: Optional[int] = None
    job_id: int
    user_id: int
    message: str


class ResponseUpdateSchema(BaseModel):
    job_id: Optional[int] = None
    user_id: Optional[int] = None
    message: Optional[str] = None


class ResponseCreateSchema(BaseModel):
    id: Optional[int] = None
    job_id: int
    user_id: int
    message: str

