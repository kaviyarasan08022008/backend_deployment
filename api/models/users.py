from sqlalchemy import Column, Integer, String
from db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    user_name = Column(String, unique=True, index=True)
    password = Column(String)

    state = Column(String)
    district = Column(String)
    village_town = Column(String)

    user_role = Column(String)  # admin / collector / user
