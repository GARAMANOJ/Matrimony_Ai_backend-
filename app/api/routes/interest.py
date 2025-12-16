# In app/api/routes/interest.py

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_ # <-- Import select, and_, or_

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.interest import Interest
from app.models.match import Match
from app.models.user import User # <-- Import User model
from app.schemas.interest import InterestCreate

router = APIRouter()

@router.post("/interest/send")
async def send_interest(
    to_user_id: int,
    # --- FIX 1: Use async def and accept the User object ---
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if current_user.id == to_user_id:
        raise HTTPException(status_code=400, detail="Cannot send interest to yourself")

    # --- FIX 2: Use the new select() syntax for querying ---
    stmt = select(Interest).where(
        and_(Interest.from_user_id == current_user.id, Interest.to_user_id == to_user_id)
    )
    result = await db.execute(stmt)
    existing = result.scalar_one_or_none()

    if existing:
        raise HTTPException(status_code=400, detail="Interest already sent")

    interest = Interest(
        from_user_id=current_user.id,
        to_user_id=to_user_id,
        status="pending"
    )

    db.add(interest)
    # --- FIX 3: Await the commit ---
    await db.commit()

    return {"message": "Interest sent successfully"}


@router.post("/interest/accept")
async def accept_interest(
    from_user_id: int = Query(..., description="Sender user id"),
    # --- FIX 4: Use async def and accept the User object ---
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Find pending interest sent TO logged-in user
    stmt = select(Interest).where(
        and_(
            Interest.from_user_id == from_user_id,
            Interest.to_user_id == current_user.id,
            Interest.status == "pending"
        )
    )
    result = await db.execute(stmt)
    interest = result.scalar_one_or_none()

    if not interest:
        raise HTTPException(status_code=404, detail="Interest not found")

    # Update interest status
    interest.status = "accepted"

    # Prevent duplicate match
    match_stmt = select(Match).where(
        or_(
            and_(Match.user1_id == from_user_id, Match.user2_id == current_user.id),
            and_(Match.user1_id == current_user.id, Match.user2_id == from_user_id)
        )
    )
    match_result = await db.execute(match_stmt)
    existing_match = match_result.scalar_one_or_none()

    if not existing_match:
        new_match = Match(
            user1_id=from_user_id,
            user2_id=current_user.id
        )
        db.add(new_match)

    # --- FIX 5: Await the commit ---
    await db.commit()

    return {"message": "Interest accepted. Match created"}

@router.post("/interest/reject")
async def reject_interest(
    from_user_id: int = Query(..., description="Sender user id"),
    # --- FIX 6: Use async def and accept the User object ---
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Interest).where(
        and_(
            Interest.from_user_id == from_user_id,
            Interest.to_user_id == current_user.id,
            Interest.status == "pending"
        )
    )
    result = await db.execute(stmt)
    interest = result.scalar_one_or_none()

    if not interest:
        raise HTTPException(status_code=404, detail="Interest not found")

    interest.status = "rejected"
    # --- FIX 7: Await the commit ---
    await db.commit()

    return {"message": "Interest rejected"}