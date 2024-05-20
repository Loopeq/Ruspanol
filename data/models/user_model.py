import enum

from sqlalchemy import ForeignKey, String

from data.custom_types import intpk, created_at
from data.database import Base
from sqlalchemy.orm import Mapped, mapped_column


class UserModel(Base):
    __tablename__ = "user"

    id: Mapped[intpk]
    tg_id: Mapped[str] = mapped_column(unique=True, nullable=False)
    created_at: Mapped[created_at]
