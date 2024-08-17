from sqlalchemy import Column, Identity, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models import Base


class DBUser(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, Identity(), primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    surname: Mapped[str] = mapped_column(String(255), nullable=False)
