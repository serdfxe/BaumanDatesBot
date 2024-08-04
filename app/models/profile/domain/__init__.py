from sqlalchemy import BigInteger, Boolean, Column, ForeignKey, Integer, String
from utils.db import Base


class Profile(Base):
    __tablename__ = 'profile'
    
    user_id = Column(BigInteger, ForeignKey('user.id'), nullable=False, primary_key=True)
    
    name = Column(String(30), nullable=False)
    age = Column(Integer, nullable=False)
    sex = Column(String(10), nullable=False)
    description = Column(String(250))
    photo = Column(String)


class ViewedProfile(Base):
    __tablename__ = 'viewed_profile'
    
    observer_id = Column(Integer, ForeignKey('user.id'), nullable=False, primary_key=True)
    target_id = Column(Integer, ForeignKey('user.id'), nullable=False, primary_key=True)
    status = Column(Boolean, nullable=False)
