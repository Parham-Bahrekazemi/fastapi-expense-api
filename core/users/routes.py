from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from passlib.context import CryptContext

from app.database import get_db

from users.model import UserModel, UserRole
from users.schemas import (
    UserCreateSchema,
    UserLoginSchema,
    TokenResponseSchema,
    RefreshTokenRequestSchema,
    UserResponseSchema,
)
from auth.permissions import require_admin
from auth.jwt import create_access_token, create_refresh_token, decode_refresh_token


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
)
def register(
    user_schema: UserCreateSchema,
    db: Session = Depends(get_db),
):

    existing_user = (
        db.query(UserModel).filter(UserModel.name == user_schema.name).first()
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists",
        )

    hashed_password = pwd_context.hash(user_schema.password)

    user = UserModel(
        name=user_schema.name,
        password_hash=hashed_password,
        role=UserRole.USER,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {"message": "User created successfully"}


@router.post(
    "/login",
    response_model=TokenResponseSchema,
)
def login(
    user_schema: UserLoginSchema,
    db: Session = Depends(get_db),
):

    user = db.query(UserModel).filter(UserModel.name == user_schema.name).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    if not pwd_context.verify(
        user_schema.password,
        user.password_hash,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is inactive",
        )

    access_token = create_access_token(
        user_id=user.id,
        role=user.role.value,
    )

    refresh_token = create_refresh_token(
        user_id=user.id,
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.post("/refresh")
def refresh_token(
    data: RefreshTokenRequestSchema,
    db: Session = Depends(get_db),
):

    user_id = decode_refresh_token(data.refresh_token)

    user = db.query(UserModel).filter(UserModel.id == user_id).first()

    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    new_access_token = create_access_token(
        user_id=user.id,
        role=user.role.value,
    )

    return {
        "access_token": new_access_token,
        "token_type": "bearer",
    }


@router.get(
    "/users",
    response_model=list[UserResponseSchema],
    status_code=status.HTTP_200_OK,
)
def get_users(
    _: UserModel = Depends(require_admin),
    db: Session = Depends(get_db),
):

    users = db.query(UserModel).all()

    return users


@router.get(
    "/users/{user_id}",
    response_model=UserResponseSchema,
    status_code=status.HTTP_200_OK,
)
def get_user(
    user_id: int,
    _: UserModel = Depends(require_admin),
    db: Session = Depends(get_db),
):

    user = db.query(UserModel).filter(UserModel.id == user_id).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user


@router.delete(
    "/users/{user_id}",
    status_code=status.HTTP_200_OK,
)
def delete_user(
    user_id: int,
    current_user: UserModel = Depends(require_admin),
    db: Session = Depends(get_db),
):

    user = db.query(UserModel).filter(UserModel.id == user_id).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    if user.role == UserRole.SUPER_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Super admin cannot be deleted",
        )

    if current_user.id == user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You cannot delete your own account",
        )

    if current_user.role == UserRole.ADMIN and user.role != UserRole.USER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admins can only delete normal users",
        )

    db.delete(user)
    db.commit()

    return {
        "message": "User deleted successfully",
    }
