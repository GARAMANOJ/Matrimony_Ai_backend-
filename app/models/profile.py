from sqlalchemy import Column, Integer, String, ForeignKey
from app.core.database import Base

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String)
    age = Column(Integer)
    religion = Column(String)
    education = Column(String)
    location = Column(String)
