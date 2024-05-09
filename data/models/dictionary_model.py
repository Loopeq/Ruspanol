from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from data.custom_types import intpk
from data.database import Base


class DictionaryModel(Base):
    __tablename__ = "dictionary"

    id: Mapped[intpk]
    tg_id: Mapped[str] = mapped_column(ForeignKey("user.tg_id", ondelete="CASCADE"))
    phrase_id: Mapped[int] = mapped_column(ForeignKey("phrase.id"))
    score: Mapped[int] = mapped_column(default=0)



