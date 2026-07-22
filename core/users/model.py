from sqlalchemy import Column, Integer, String, Boolean, Enum
from sqlalchemy.orm import relationship

from app.database import Base

import enum


class UserRole(str, enum.Enum):
    USER = "user"
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)

    name = Column(String, nullable=False)

    password_hash = Column(String, nullable=False)

    role = Column(Enum(UserRole), default=UserRole.USER)

    is_active = Column(Boolean, default=True)

    expenses = relationship(
        "ExpenseModel",
        back_populates="user",
        cascade="all, delete-orphan",
    )
