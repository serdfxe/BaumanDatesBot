from sqlalchemy.orm import sessionmaker
from utils.db import engine


Session = sessionmaker(bind=engine)
