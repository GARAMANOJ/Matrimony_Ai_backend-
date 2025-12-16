# In app/api/routes/profile.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.profile import Profile
from app.models.user import User # <-- 1. Make sure to import the User model
from app.schemas.profile import ProfileCreate, ProfileOut

router = APIRouter()

@router.post("/profile", response_model=ProfileOut)
async def create_profile(
    profile: ProfileCreate,
    # --- FIX 1: Change the dependency parameter ---
    # It should accept a User object, not an integer.
    current_user: User = Depends(get_current_user), 
    db: AsyncSession = Depends(get_db)
):
    # --- FIX 2: Use the ID from the User object ---
    stmt = select(Profile).where(Profile.user_id == current_user.id)
    result = await db.execute(stmt)
    existing = result.scalar_one_or_none()

    if existing:
        raise HTTPException(status_code=400, detail="Profile already exists")

    # Create the new profile
    new_profile = Profile(user_id=current_user.id, **profile.dict())
    db.add(new_profile)
    await db.commit()
    await db.refresh(new_profile)
    
    return new_profile