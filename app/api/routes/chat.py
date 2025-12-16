from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
# --- CHANGE 1: Import async components ---
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.schemas.user import UserCreate
from app.models.user import User
from app.core.database import get_db
from app.core.security import hash_password, verify_password, create_access_token

router = APIRouter()

# ---------------- REGISTER ----------------
# --- CHANGE 2: Make function async and use AsyncSession ---
@router.post("/register")
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    # --- CHANGE 3: Use the new select() syntax for querying ---
    stmt = select(User).where(User.email == user.email)
    result = await db.execute(stmt)
    existing = result.scalar_one_or_none() # Use .scalar_one_or_none() to get one result or None

    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create a new user instance
    new_user = User(
        email=user.email,
        password=hash_password(user.password)
    )
    
    db.add(new_user)
    # --- CHANGE 4: Await the commit and refresh ---
    await db.commit()
    await db.refresh(new_user) # Refresh to get the new user's ID from the DB

    return {"msg": "Registered successfully"}


# ---------------- LOGIN (FIXED) ----------------
# --- CHANGE 5: Make function async and use AsyncSession ---
@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    # NOTE: OAuth2PasswordRequestForm uses "username" field, but we are expecting an email.
    # We'll search for the user by email.
    # --- CHANGE 6: Use the new select() syntax for querying ---
    stmt = select(User).where(User.email == form_data.username)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(data={"sub": str(user.id)}) # Use "sub" for subject, which is standard practice

    return {
        "access_token": token,
        "token_type": "bearer"
    }
