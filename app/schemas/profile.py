from pydantic import BaseModel

class ProfileCreate(BaseModel):
    name: str
    age: int
    religion: str
    education: str
    location: str

class ProfileOut(ProfileCreate):
    id: int
    user_id: int

    class Config:
        from_attributes = True
