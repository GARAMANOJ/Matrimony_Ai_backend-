from pydantic import BaseModel

class PreferenceCreate(BaseModel):
    min_age: int
    max_age: int
    religion: str
    education: str
    location: str

class PreferenceOut(PreferenceCreate):
    id: int
    user_id: int

    class Config:
        from_attributes = True
