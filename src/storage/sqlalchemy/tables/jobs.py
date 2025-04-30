from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from storage.sqlalchemy.client import Base


class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(primary_key=True, comment="Идентификатор вакансии")
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), comment="Идентификатор пользователя"
    )

    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text())
    salary_from: Mapped[str] = mapped_column(String(50))
    salary_to: Mapped[str] = mapped_column(String(50))
    is_active: Mapped[bool] = mapped_column(Boolean(), default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(), default=datetime.utcnow)

    user: Mapped["User"] = relationship(back_populates="jobs")  # noqa
    responses: Mapped["Response"] = relationship(back_populates="job")  # noqa
