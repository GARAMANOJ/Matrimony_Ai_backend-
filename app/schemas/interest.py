from pydantic import BaseModel

class InterestCreate(BaseModel):
    to_user_id: int
