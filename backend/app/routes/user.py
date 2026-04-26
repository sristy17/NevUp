from fastapi import APIRouter, Depends, HTTPException
from app.auth.deps import get_current_user

router = APIRouter()

@router.get("/users/{userId}")
def get_user(userId: str, user=Depends(get_current_user)):
    if user["sub"] != userId:
        raise HTTPException(status_code=403, detail="FORBIDDEN")

    return {"message": "Access granted", "userId": userId}