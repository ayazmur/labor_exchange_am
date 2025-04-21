import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, constr, model_validator
from typing_extensions import Self
# id: int
# title: Mapped[str] = mapped_column(String(255))
#     description: Mapped[str] = mapped_column(Text())
#     salary_from: Mapped[str] = mapped_column(String(50))
#     salary_to: Mapped[str] = mapped_column(String(50))
#     is_active: Mapped[bool] = mapped_column(Boolean(), default=True)
#     created_at: Mapped[datetime] = mapped_column(DateTime(), default=datetime.utcnow)

class JobSchema(BaseModel):
    id: Optional[int] = None
    title: str
    description: str
    salary_from: str
    salary_to: str
    is_active: bool
    created_at: datetime.datetime.utcnow()



class JobUpdateSchema(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    salary_from: Optional[str] = None
    salary_to: Optional[str] = None
    is_active: Optional[bool] = None
    created_at: Optional[datetime.datetime.utcnow()] = None




class JobCreateSchema(BaseModel):
    id: Optional[int] = None
    title: str
    description: str
    salary_from: str
    salary_to: str
    is_active: bool
    created_at: datetime.datetime.utcnow()

