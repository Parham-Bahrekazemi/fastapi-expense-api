from fastapi import Depends, HTTPException, status

from users.model import UserModel, UserRole

from auth.dependencies import get_current_user


def require_admin(current_user: UserModel = Depends(get_current_user)):

    if current_user.role not in [
        UserRole.ADMIN,
        UserRole.SUPER_ADMIN,
    ]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )

    return current_user


def require_super_admin(current_user: UserModel = Depends(get_current_user)):

    if current_user.role != UserRole.SUPER_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Super admin access required",
        )

    return current_user
