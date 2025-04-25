import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, constr, model_validator
from typing_extensions import Self


class JobCreateSchema(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    salary_from: Optional[str] = None
    salary_to: Optional[str] = None
    is_active: bool = True


class JobSchema(JobCreateSchema):
    id: int
    user_id: int


class JobUpdateSchema(JobCreateSchema):
    id: int
