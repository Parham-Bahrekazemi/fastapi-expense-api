from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from sqlalchemy.orm import Session

from app.database import get_db

from users.model import UserModel, UserRole
from auth.permissions import require_super_admin


router = APIRouter(
    prefix="/super-admin",
    tags=["Super Admin"],
)


@router.patch(
    "/users/{user_id}/make-admin",
    status_code=status.HTTP_200_OK,
)
def promote_to_admin(
    user_id: int,
    _: UserModel = Depends(require_super_admin),
    db: Session = Depends(get_db),
):

    user = db.query(UserModel).filter(UserModel.id == user_id).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    if user.role == UserRole.SUPER_ADMIN:
        raise HTTPException(
            status_code=400,
            detail="Cannot modify super admin",
        )

    if user.role == UserRole.ADMIN:
        raise HTTPException(
            status_code=400,
            detail="User is already admin",
        )

    user.role = UserRole.ADMIN

    db.commit()
    db.refresh(user)

    return {
        "message": "User promoted to admin successfully",
        "user_id": user.id,
    }


@router.patch(
    "/users/{user_id}/revoke-admin",
    status_code=status.HTTP_200_OK,
)
def revoke_admin(
    user_id: int,
    _: UserModel = Depends(require_super_admin),
    db: Session = Depends(get_db),
):

    user = db.query(UserModel).filter(UserModel.id == user_id).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    if user.role == UserRole.SUPER_ADMIN:
        raise HTTPException(
            status_code=403,
            detail="Cannot revoke super admin",
        )

    if user.role == UserRole.USER:
        raise HTTPException(
            status_code=400,
            detail="User is not admin",
        )

    user.role = UserRole.USER

    db.commit()
    db.refresh(user)

    return {
        "message": "Admin role revoked successfully",
        "user_id": user.id,
    }
