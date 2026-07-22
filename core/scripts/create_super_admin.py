from app.database import SessionLocal
from users.model import UserModel, UserRole
from expenses.model import ExpenseModel
from passlib.context import CryptContext


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


db = SessionLocal()


admin = UserModel(
    name="owner",
    password_hash=pwd_context.hash("StrongPassword123"),
    role=UserRole.SUPER_ADMIN,
    is_active=True,
)


db.add(admin)
db.commit()

print("Super admin created")
