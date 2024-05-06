from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from data.custom_types import intpk
from data.database import Base


class PhrasesModel(Base):
    __tablename__ = "phrase"

    id: Mapped[intpk]
    ru: Mapped[str] = mapped_column(String(128), nullable=False)
    es: Mapped[str] = mapped_column(String(128), nullable=False)
