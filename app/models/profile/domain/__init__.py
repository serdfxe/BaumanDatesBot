from sqlalchemy import BigInteger, Column, Enum, ForeignKey, Integer, String
from utils.db import Base
import enum

# class SexEnum(enum.Enum):
#     male = "Male"
#     female = "Female"
#     none = ""

class Profile(Base):
    __tablename__ = 'profile'
    
    user_id = Column(BigInteger, ForeignKey('user.id'), nullable=False, primary_key=True)
    
    name = Column(String(30), nullable=False)
    age = Column(Integer, nullable=False)
    sex = Column(String(10), nullable=False)
    description = Column(String(250))
    photo = Column(String)
