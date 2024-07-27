from sqlalchemy import BigInteger, Column, ForeignKey, Integer, String
from utils.db import Base



class Request(Base):
    __tablename__ = 'request'
    
    id = Column(Integer, autoincrement=True, nullable=False, primary_key=True)
    user_id = Column(BigInteger, ForeignKey('user.id'), nullable=False, primary_key=True)
    request = Column(String, nullable=False)
