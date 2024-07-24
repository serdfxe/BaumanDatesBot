from sqlalchemy import BigInteger, Column, ForeignKey, Integer, String
from utils.db import Base


class Profile(Base):
    __tablename__ = 'profile'
    
    user_id = Column(BigInteger, ForeignKey('user.id'), nullable=False, primary_key=True)
    
    name = Column(String(30), nullable=False)
    age = Column(Integer, nullable=False)
    description = Column(String(250))
    photo = Column(String)
