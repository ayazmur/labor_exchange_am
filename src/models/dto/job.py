from typing import Optional

from pydantic import BaseModel


class JobUpdateDto(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    salary_from: Optional[str] = None
    salary_to: Optional[str] = None
    is_active: bool = True


class JobCreateDto(JobUpdateDto):
    user_id: int