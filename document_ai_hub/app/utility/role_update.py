from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.model import RoleUpdateRequest, RoleUpdateResponse
from app.utility.signup import get_db
from app.database.model import UserChunk
from app.utility.auth import require_role

update_role_router = APIRouter()

@update_role_router.put("/update-role/{user_id}")
def update_user_role(
    user_id: int,
    role_update: RoleUpdateRequest,
    db: Session = Depends(get_db),
    user = Depends(require_role("admin")),
):
    user = db.query(UserChunk).filter(UserChunk.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.role = role_update.role
    db.commit()
    db.refresh(user)

    return RoleUpdateResponse(
        id=user.id,
        user_name=user.user_name,
        role=user.role
    )