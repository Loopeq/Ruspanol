from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from data.custom_types import intpk
from data.database import Base


class PhrasesModel(Base):
    __tablename__ = "phrase"

    id: Mapped[intpk]
    ru: Mapped[str] = mapped_column(String(128), nullable=False)
    es: Mapped[str] = mapped_column(String(128), nullable=False)


class UserPhrasesProgressModel(Base):
    __tablename__ = "user_phrases_progress"

    id: Mapped[intpk]
    tg_id: Mapped[str] = mapped_column(ForeignKey("user.tg_id", ondelete="CASCADE"))
    phrase_id: Mapped[int] = mapped_column(ForeignKey("phrase.id"), default=1)
