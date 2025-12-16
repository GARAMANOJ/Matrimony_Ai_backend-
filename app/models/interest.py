from sqlalchemy import Column, Integer, ForeignKey, String
from app.core.database import Base

class Interest(Base):
    __tablename__ = "interests"

    id = Column(Integer, primary_key=True)
    from_user_id = Column(Integer, ForeignKey("users.id"))
    to_user_id = Column(Integer, ForeignKey("users.id"))
    status = Column(String, default="pending")  
    # pending | accepted | rejected
