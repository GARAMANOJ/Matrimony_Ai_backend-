from sqlalchemy import Column, Integer, String, ForeignKey
from app.core.database import Base

class Preference(Base):
    __tablename__ = "preferences"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    min_age = Column(Integer)
    max_age = Column(Integer)
    religion = Column(String)
    education = Column(String)   
    location = Column(String)
