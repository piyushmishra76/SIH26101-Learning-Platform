from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.Database.connection import get_db
from app.models.user import User
from app.utils.dependencies import get_current_admin


router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)
@router.get("/users")
def get_all_users(
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    users = (
        db.query(User)
        .order_by(User.id)
        .all()
    )

    return [
        {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "designation": user.designation,
            "department": user.department
        }
        for user in users
    ]