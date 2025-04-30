from typing import Optional

from pydantic import BaseModel, EmailStr, constr, model_validator, Field
from typing_extensions import Self


class UserSchema(BaseModel):
    """
    Схема пользователя
    """
    id: Optional[int] = Field(description="Идентификатор пользователя")
    name: str = Field(description="Имя пользователя")
    email: EmailStr = Field(description="Email адрес")
    is_company: bool = Field(description="Флаг компании")

class UserUpdateSchema(BaseModel):
    """
    Схема обновления пользователя
    """
    name: str = Field(description="Имя пользователя")
    email: EmailStr = Field(description="Email адрес")
    is_company: bool = Field(description="Флаг компании")


class UserCreateSchema(BaseModel):
    """
    Схема созания пользователя
    """
    id: Optional[int] = Field(description="Идентификатор пользователя")
    name: str = Field(description="Имя пользователя")
    password: constr(min_length=8) = Field(description="Пароль")
    password2: str = Field(description="Пароль")
    is_company: bool = Field(default=False, description="Флаг компаниии")

    @model_validator(mode="after")
    def password_match(self) -> Self:
        pw1 = self.password
        pw2 = self.password2
        if pw1 is not None and pw2 is not None and pw1 != pw2:
            raise ValueError("passwords do not match")
        return self
