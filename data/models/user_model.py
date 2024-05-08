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


class Role(enum.Enum):
    user = "user"
    assistant = "assistant"
    system = "system"


class UserHistModel(Base):
    __tablename__ = "user_hist_gpt"

    id: Mapped[intpk]
    tg_id: Mapped[str] = mapped_column(ForeignKey("user.tg_id", ondelete="CASCADE"))
    message: Mapped[str] = mapped_column(String(128))
    role: Mapped[Role]
