from sqlalchemy import Column, Integer, String, Identity
from sqlalchemy.orm import relationship, Mapped, mapped_column

from db.models import Base


class DBUser(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, Identity(), init=False, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    surname: Mapped[str] = mapped_column(String(255), nullable=False)
