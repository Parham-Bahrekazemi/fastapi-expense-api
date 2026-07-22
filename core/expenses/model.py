from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.database import Base


class ExpenseModel(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True)

    description = Column(String)

    amount = Column(Float)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
    )

    user = relationship("UserModel", back_populates="expenses")
