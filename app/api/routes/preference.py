# In app/api/routes/preference.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select # <-- Import select

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.preference import Preference
from app.models.user import User # <-- Import User model
from app.schemas.preference import PreferenceCreate, PreferenceOut

router = APIRouter()

@router.post("/preference", response_model=PreferenceOut)
async def create_or_update_preference(
    pref: PreferenceCreate,
    # --- FIX 1: Use async def and accept the User object ---
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # --- FIX 2: Use the new select() syntax for querying ---
    stmt = select(Preference).where(Preference.user_id == current_user.id)
    result = await db.execute(stmt)
    existing = result.scalar_one_or_none()

    if existing:
        # Update preference
        for key, value in pref.dict().items():
            setattr(existing, key, value)
        # --- FIX 3: Await the commit and refresh ---
        await db.commit()
        await db.refresh(existing)
        return existing

    # Create new preference
    new_preference = Preference(user_id=current_user.id, **pref.dict())
    db.add(new_preference)
    # --- FIX 4: Await the commit and refresh ---
    await db.commit()
    await db.refresh(new_preference)
    return new_preference



@router.get("/preference/me", response_model=PreferenceOut)
async def get_my_preference(
    # --- FIX 5: Use async def and accept the User object ---
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # --- FIX 6: Use the new select() syntax for querying ---
    stmt = select(Preference).where(Preference.user_id == current_user.id)
    result = await db.execute(stmt)
    pref = result.scalar_one_or_none()

    if not pref:
        raise HTTPException(status_code=404, detail="Preference not found")

    return pref