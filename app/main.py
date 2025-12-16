from fastapi import FastAPI

# Database
from app.core.database import Base, engine

# 🔥 IMPORT ALL MODELS (VERY IMPORTANT)
from app.models.user import User
from app.models.profile import Profile
from app.models.preference import Preference
from app.models.interest import Interest
from app.models.match import Match

# Create FastAPI app
app = FastAPI(
    title="AI Matrimony",
    description="Find your perfect match with AI.",
    version="1.0.0"
)

# ✅ CREATE TABLES (ASYNC SAFE)
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Database tables created")

# ✅ CLOSE ENGINE PROPERLY
@app.on_event("shutdown")
async def shutdown():
    print("🛑 Shutting down application...")
    await engine.dispose()
    print("✅ Database engine closed")

# Routers
from app.api.routes.auth import router as auth_router
from app.api.routes.profile import router as profile_router
from app.api.routes.preference import router as preference_router
from app.api.routes.match import router as match_router
from app.api.routes.interest import router as interest_router

app.include_router(auth_router, prefix="/api/auth")
app.include_router(profile_router, prefix="/api")
app.include_router(preference_router, prefix="/api")
app.include_router(match_router, prefix="/api/match")
app.include_router(interest_router, prefix="/api/interest")
