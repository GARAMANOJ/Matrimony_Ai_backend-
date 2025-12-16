# In app/api/routes/match.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select # <-- Import select

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.profile import Profile
from app.models.preference import Preference
from app.models.user import User # <-- Import User model
from app.services.match_engine import calculate_match

router = APIRouter()

@router.get("/suggestions")
async def get_match_suggestions(
    # --- FIX 1: Use async def and accept the User object ---
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # --- FIX 2: Use the new select() syntax for querying ---
    # Get my profile
    stmt_my_profile = select(Profile).where(Profile.user_id == current_user.id)
    result_my_profile = await db.execute(stmt_my_profile)
    my_profile = result_my_profile.scalar_one_or_none()

    # Get my preference
    stmt_pref = select(Preference).where(Preference.user_id == current_user.id)
    result_pref = await db.execute(stmt_pref)
    pref = result_pref.scalar_one_or_none()

    if not my_profile:
        raise HTTPException(status_code=400, detail="Profile not created")

    if not pref:
        raise HTTPException(status_code=400, detail="Preference not created")

    # 🔥 TRY TO GET OTHER PROFILES
    stmt_others = select(Profile).where(Profile.user_id != current_user.id)
    result_others = await db.execute(stmt_others)
    others = result_others.scalars().all()

    # 🔥 FALLBACK FOR DEVELOPMENT (IMPORTANT)
    if not others:
        stmt_all = select(Profile)
        result_all = await db.execute(stmt_all)
        others = result_all.scalars().all()   # include self for demo/testing

    results = []

    for p in others:
        score = calculate_match(pref, p)

        results.append({
            "user_id": p.user_id,
            "name": p.name,
            "age": p.age,
            "religion": p.religion,
            "education": p.education,
            "location": p.location,
            "match_percentage": score
        })

    return results