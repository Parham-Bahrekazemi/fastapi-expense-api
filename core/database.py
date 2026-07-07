from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

SQLALCHEMY_DATABASE_URL = "sqlite:///./sqlite.db"


engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)


SessionLocal = sessionmaker(autoflush=False, expire_on_commit=False, bind=engine)


Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String())
    expenses = relationship(
        "Expense",
        back_populates="user",
    )


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )
    user = relationship(
        "User",
        back_populates="expenses",
    )
    description = Column(String())
    amount = Column(Float)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
