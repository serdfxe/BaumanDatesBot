from sqlalchemy import Column, BigInteger, ForeignKey, String, Boolean

from utils.db import Base
from utils.db.mixins import TimestampMixin


class User(Base, TimestampMixin):
    __tablename__ = 'users'
    
    id = Column(BigInteger, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    username = Column(String)
    
    role = Column(String)
    banned = Column(Boolean)
    
    # email = Column(String)
    # verified = Column(Boolean)


# class MailConfimationCode(Base, DBTool):
#     __tablename__ = 'mail_confimation_codes'
    
#     user_id = Column(BigInteger, ForeignKey('users.id'), primary_key=True)
#     email = Column(String)
#     code = Column(String)
