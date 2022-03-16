from typing import Optional, List

from fastapi import APIRouter, Depends
from managers.auth import oauth2_schema, is_admin
from managers.user import UserManager
from models import RoleType
from schemas.response.user import UserOut

router = APIRouter(tags=["Users"])


@router.get("/users/", dependencies=[Depends(oauth2_schema), Depends(is_admin)], response_model=List[UserOut])
async def get_users(email: Optional[str] = None):
    if email:
        return await UserManager.get_user_by_email(email)
    return await UserManager.get_all_users()


@router.put("/user/{user_id}/make_admin",
            dependencies=[Depends(oauth2_schema), Depends(is_admin)]
            )
async def make_admin(user_id: int):
    await UserManager.change_role(RoleType.admin, user_id)


@router.put("/user/{user_id}/make_approver",
            dependencies=[Depends(oauth2_schema), Depends(is_admin)]
            )
async def make_admin(user_id: int):
    await UserManager.change_role(RoleType.approver, user_id)